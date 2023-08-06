from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import List
import zipfile as zf
from pathlib import Path
import pandas as pd
import requests
from . import config as cf

URL_DFP = "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/"
URL_ITR = "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/"

CVM_DF_PATH = cf.DATA_PATH / "cvm_df.pkl"


def get_cvm_df() -> pd.DataFrame:
    """Get CVM files metadata."""
    if CVM_DF_PATH.is_file():
        cvm_df = pd.read_pickle(CVM_DF_PATH)
    else:
        columns = ["filename", "file_size", "etag", "last_modified"]
        cvm_df = pd.DataFrame(columns=columns)
    return cvm_df


def list_urls() -> List[str]:
    """Update the CVM Portal file base.
    Urls with CVM raw files:
    http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/
    http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/
    Links example:
    http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_2020.zip
    http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_2020.zip
    Throughout 2021, there are already DFs for the year 2022 because the
    company's social calendar may not necessarily coincide with the official
    calendar. Because of this, 2 is added to the current year (the second limit
    of the range function is exclusive)
    """
    first_year = 2010  # First year avaible at CVM Portal.
    # Next year files will appear during current year.
    last_year = pd.Timestamp.now().year + 1
    years = list(range(first_year, last_year + 1))
    first_year_itr = last_year - 3
    urls = []
    for year in years:
        filename = f"dfp_cia_aberta_{year}.zip"
        url = f"{URL_DFP}{filename}"
        urls.append(url)
        if year >= first_year_itr:
            filename = f"itr_cia_aberta_{year}.zip"
            url = f"{URL_ITR}{filename}"
            urls.append(url)
    return urls


def update_raw_file(url: str) -> Path:
    """Update raw file from CVM portal. Return a Path if file is updated."""
    cvm_filepath = Path(cf.RAW_DIR, url[-23:])  # filename = url final
    with requests.Session() as s:
        r = s.get(url, stream=True)
        if r.status_code != requests.codes.ok:
            return None

    if Path.exists(cvm_filepath):
        local_file_size = cvm_filepath.stat().st_size
    else:
        local_file_size = 0
    url_file_size = int(r.headers["Content-Length"])
    if local_file_size == url_file_size:
        # File is already updated
        return None
    with cvm_filepath.open(mode="wb") as f:
        f.write(r.content)

    # headers["Last-Modified"] -> 'Wed, 23 Jun 2021 12:19:24 GMT'
    ts_server = pd.to_datetime(
        r.headers["Last-Modified"], format="%a, %d %b %Y %H:%M:%S %Z"
    )
    # Store URL files metadata in a DataFrame
    cvm_df = get_cvm_df()
    cvm_df.loc[pd.Timestamp.now()] = [
        cvm_filepath.name,
        r.headers["Content-Length"],
        r.headers["ETag"],
        ts_server,
    ]
    cvm_df.to_pickle(CVM_DF_PATH)
    return cvm_filepath


def update_raw_files(urls: str) -> List[Path]:
    """Update local CVM raw files asynchronously."""
    with ThreadPoolExecutor() as executor:
        results = executor.map(update_raw_file, urls)
    updated_filepaths = [r for r in results if r is not None]
    return updated_filepaths


def pre_process_file(cvm_filepath: Path) -> Path:
    """Read annual file, process it, save the result and return the file path."""
    df = pd.DataFrame()
    annual_zipfile = zf.ZipFile(cvm_filepath)
    child_filenames = annual_zipfile.namelist()

    df_list = []
    for child_filename in child_filenames[1:]:
        child_file = annual_zipfile.open(child_filename)

        # Only "DT_INI_EXERC" and "COLUNA_DF" have missing values.
        child_df = pd.read_csv(
            child_file,
            sep=";",
            encoding="iso-8859-1",
            true_values=["S"],
            false_values=["N"],
        )
        # Currency column has only one value (BRL) so it is not necessary.
        child_df = child_df.drop(columns=["MOEDA"])

        # There are two types of CVM files: DFP (annual) and ITR (quarterly).
        if cvm_filepath.name.startswith("dfp"):
            child_df["report_type"] = "annual"
        else:
            child_df["report_type"] = "quarterly"

        df_list.append(child_df)

    df = pd.concat(df_list, ignore_index=True)

    # Convert string columns to categorical.
    columns = df.select_dtypes(include="object").columns
    df[columns] = df[columns].astype("category")
    return df


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    """Process a raw dataframe and return a formatted dataframe."""
    columns_translation = {
        "CNPJ_CIA": "co_fiscal_id",
        "DT_REFER": "period_reference",
        "VERSAO": "report_version",
        "DENOM_CIA": "co_name",
        "CD_CVM": "co_id",
        "GRUPO_DFP": "report_group",
        "ESCALA_MOEDA": "currency_unit",
        "ORDEM_EXERC": "period_order",
        "DT_FIM_EXERC": "period_end",
        "CD_CONTA": "acc_code",
        "DS_CONTA": "acc_name",
        "VL_CONTA": "acc_value",
        "ST_CONTA_FIXA": "acc_fixed",
        "DT_INI_EXERC": "period_begin",
        "COLUNA_DF": "equity_statement_column",
    }
    df.rename(columns=columns_translation, inplace=True)

    adjust_data_types = {
        "co_id": "UInt32",  # max. value = 600_000
        "report_version": "UInt8",  # values are 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        "period_begin": "datetime64[ns]",
        "period_end": "datetime64[ns]",
        "period_reference": "datetime64[ns]",
    }
    df = df.astype(adjust_data_types)
    # currency_unit values are ['MIL', 'UNIDADE']
    map_dict = {"UNIDADE": 1, "MIL": 1000}
    df["currency_unit"] = df["currency_unit"].map(map_dict).astype(int)

    # Do not ajust acc_value for 3.99 codes.
    df["acc_value"] = df["acc_value"].where(
        df["acc_code"].str.startswith("3.99"),
        df["acc_value"] * df["currency_unit"],
    )
    df.drop(columns=["currency_unit"], inplace=True)

    # "period_order" values are: 'ÚLTIMO', 'PENÚLTIMO'
    map_dict = {"ÚLTIMO": "LAST", "PENÚLTIMO": "PREVIOUS"}
    df["period_order"] = df["period_order"].map(map_dict)
    """
    acc_method -> Financial Statemen Type
    Consolidated and Separate Financial Statements (IAS 27/2003)
    df['GRUPO_DFP'].unique() result:
        'DF Consolidado - Balanço Patrimonial Ativo',
        'DF Consolidado - Balanço Patrimonial Passivo',
        'DF Consolidado - Demonstração das Mutações do Patrimônio Líquido',
        'DF Consolidado - Demonstração de Resultado Abrangente',
        'DF Consolidado - Demonstração de Valor Adicionado',
        'DF Consolidado - Demonstração do Fluxo de Caixa (Método Indireto)',
        'DF Consolidado - Demonstração do Resultado',
        'DF Individual - Balanço Patrimonial Ativo',
        'DF Individual - Balanço Patrimonial Passivo',
        'DF Individual - Demonstração das Mutações do Patrimônio Líquido',
        'DF Individual - Demonstração de Resultado Abrangente',
        'DF Individual - Demonstração de Valor Adicionado',
        'DF Individual - Demonstração do Fluxo de Caixa (Método Indireto)',
        'DF Individual - Demonstração do Resultado',
    Hence, with string position 3:6 we can make:
    if == 'Con' -> consolidated statement
    if == 'Ind' -> separate statement
    """
    df["acc_method"] = (
        df["report_group"].str[3:6].map({"Con": "consolidated", "Ind": "separate"})
    )
    # 'GRUPO_DFP' data can be inferred from 'acc_code'
    df.drop(columns=["report_group"], inplace=True)
    # Correct/harmonize some account texts.
    df["acc_name"].replace(to_replace=["\xa0ON\xa0", "On"], value="ON", inplace=True)
    # Remove duplicated accounts
    cols = list(df.columns)
    # cols.remove("acc_value")
    df.drop_duplicates(cols, keep="last", inplace=True)
    columns_order = [
        "co_name",
        "co_id",
        "co_fiscal_id",
        "report_type",
        "report_version",
        "period_reference",
        "period_begin",
        "period_end",
        "period_order",
        "acc_code",
        "acc_name",
        "acc_method",
        "acc_fixed",
        "acc_value",
        "equity_statement_column",
    ]
    df = df[columns_order]
    # Most values in datetime and string columns are the same.
    # So these remaining columns can be converted to category.
    columns = df.select_dtypes(include=["datetime64[ns]", "object"]).columns
    df[columns] = df[columns].astype("category")

    return df


def process_file(cvm_filepath: Path) -> Path:
    """Process the annual file and return the path to the processed file."""
    df = pre_process_file(cvm_filepath)
    df = format_df(df)
    processed_filepath = cf.PROCESSED_DIR / cvm_filepath.with_suffix(".pkl.zst").name
    df.to_pickle(processed_filepath)
    return processed_filepath


def process_files(
    workers: int, cvm_filepaths: List[Path], asynchronous: bool
) -> List[Path]:
    """
    Execute function 'pre_process_file' and return
    a list with filenames for the processed files.
    """
    if asynchronous:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            results = executor.map(process_file, cvm_filepaths)
        processed_filepaths = [r for r in results]
    else:
        processed_filepaths = [
            process_file(cvm_filepath) for cvm_filepath in cvm_filepaths
        ]
    return processed_filepaths
