import os
import time
import warnings
from datetime import datetime

import pandas as pd
from tqdm import tqdm

try:
    import pubchempy as pcp

    PCP_AVAILABLE = True
except ImportError:
    PCP_AVAILABLE = False


def is_na_or_empty(value):
    nan_upper_str = [
        "",
        "-NAN",
        "NAN",
        "N/A",
        "NA",
        "<NA>",
        "#N/A",
        "#N/A N/A",
        "#NA",
        "NONE",
        "NULL",
        "-1.#IND",
        "-1.#QNAN",
        "1.#IND",
        "1.#QNAN",
    ]

    if type(value) in [list, tuple, set]:
        return len(value) == 0

    val_str = str(value).upper().strip()
    result = pd.isna(value) or (val_str in nan_upper_str)
    return result


# Pull data from PubChem
def get_chemical_metadata(
    compound,
    given_name,
    pubchem_fields=dict(),
    synonym_field=dict(),
    return_synonyms=True,
    synonym_delim="\n",
    warn_notfound_synonym=True,
):
    if len(pubchem_fields) == 0:
        pubchem_fields = {
            "pubchem_cid": (float, "cid"),
            "chemical_IUPAC": (str, "iupac_name"),
            "chemical_SMILES": (str, "canonical_smiles"),
            "chemical_molecular_formula": (str, "molecular_formula"),
            "chemical_molecular_weight": (float, "molecular_weight"),
        }

    if len(synonym_field) == 0:
        synonym_field = {"chemical_synonyms": "synonyms"}
    assert len(synonym_field) == 1, "`synonym_field` can only have one field"
    ndx_syn_field = list(synonym_field.keys())[0]
    pcp_syn_field = synonym_field[ndx_syn_field]

    metadata = {
        ndx_field: type_caster(getattr(compound, pcp_field))
        for ndx_field, (type_caster, pcp_field) in pubchem_fields.items()
    }

    metadata[ndx_syn_field] = ""
    warn_mesg = ""
    if return_synonyms:
        syns = synonym_delim.join(getattr(compound, pcp_syn_field))
        metadata[ndx_syn_field] = syns

        if warn_notfound_synonym:
            if given_name.lower() not in syns.lower():
                cid = compound.cid
                warn_mesg = (
                    f"WARNING: The given name {given_name}"
                    + "could not be found in the queried synonyms. Suggestions:\n"
                    + "\tCheck your spellings or maybe this was the WRONG pair of\n "
                    + f"\t\t(pubchem_id: {compound.cid}, name: {given_name}).\n"
                    + f"\tOr visit <https://pubchem.ncbi.nlm.nih.gov/#query={cid}>"
                )
                warnings.warn(warn_mesg)

    return metadata, warn_mesg


def read_pubchem_from_file(
    cid,
    source,
    check_all_essentials=True,
    essential_columns=[
        "pubchem_cid",
        "chemical_IUPAC",
        "chemical_SMILES",
        "chemical_molecular_formula",
        "chemical_molecular_weight",
        "is_validated",
        "validation_details",
    ],
):
    assert os.path.exists(source), (
        'When `source` is not "pubchempy", '
        "it needs to be a valid CSV path to a manual file"
    )

    df_compounds = pd.read_csv(source, dtype={"pubchem_cid": "int"})
    source_columns = set(df_compounds.columns)

    assert "pubchem_cid" in source_columns, (
        f'The file "{source}" needs ' "to at least have the column `pubchem_id`"
    )

    if check_all_essentials:
        missing = set(essential_columns) - source_columns
        assert len(missing) == 0, (
            f'The file "{source}" is missing these ' f"columns = {missing}"
        )

    chem_meta = df_compounds.query("pubchem_cid == @cid")
    assert len(chem_meta) == 1, (
        "Either could not find or found duplicates of "
        f'`pubchem_cid = {cid}` in the provided file "{source}". '
        "Only ONE entry of such condition is allowed."
    )

    chem_meta = chem_meta.iloc[0]
    chem_meta["pubchem_cid"] = float(chem_meta["pubchem_cid"])
    return chem_meta


def save_pubchem_requests(
    cid_list, name_list, file_path, sleep_time=0.1, show_progress=True, **kwargs
):
    assert len(cid_list) == len(
        name_list
    ), "The length of CID and name lists need to match"
    chem_df = []
    iter_obj = list(zip(cid_list, name_list))
    if show_progress:
        iter_obj = tqdm(iter_obj)

    for cid, name in iter_obj:
        chem_df.append(request_pubchem(cid, name, source="pubchempy", **kwargs))
        if sleep_time is not None:
            time.sleep(sleep_time)

    chem_df = pd.DataFrame(chem_df)
    chem_df.to_csv(file_path, index=False)


def request_pubchem(
    cid,
    name="",
    source="pubchempy",
    return_synonyms=True,
    synonym_delim="\n",
    warn_notfound_synonym=True,
    error_notfound_cid=True,
):
    cid = int(cid)

    if source.lower() != "pubchempy":
        chem_meta = read_pubchem_from_file(cid, source)
        return chem_meta

    assert PCP_AVAILABLE, (
        "PubChemPy is not available to query. "
        "Please install with `pip install pubchempy`"
    )

    err_mesg = f'`pubchempy` had trouble finding CID="{cid}".\n'

    chem_meta = dict()

    try:
        # try to find from CID
        compound = pcp.Compound.from_cid(cid)
        validated = True
        validation_details = (
            "QUERY-WITH: PUBCHEMPY"
            + "\nTIME: "
            + datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            + "\nSTATUS: SUCCESS"
        )

        chem_meta, warn_mesg = get_chemical_metadata(
            compound=compound,
            given_name=name,
            return_synonyms=return_synonyms,
            synonym_delim=synonym_delim,
            warn_notfound_synonym=warn_notfound_synonym,
        )

        if len(warn_mesg) > 0:
            validation_details += "\n" + warn_mesg

    except:
        # if there's an error, first find compounds by name
        # then error, if there's a compound found, print the list
        # still throw an error nonetheless to be more aggressive
        attempt_cids = pcp.get_compounds(name, "name")
        if len(attempt_cids) == 0:
            err_mesg = (
                "\t"
                + err_mesg
                + f'\tCould not find any CID with name="{name} either.\n'
                + "\tPlease double check your data."
            )

        else:
            attempt_cids = [(x.cid, x.iupac_name) for x in attempt_cids]
            err_mesg = (
                "\t"
                + err_mesg
                + "\tBut was able to find the following (CID, IUPAC name).\n"
                + "\tPlease double check your data. Not moving forward to be safe.\n"
                + f"\t{attempt_cids}"
            )

        validated = False
        validation_details = (
            "QUERY-WITH: PUBCHEMPY"
            + "\nTIME: "
            + datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            + "\nSTATUS: FAILURE"
            + "\n"
            + err_mesg
        )

        if error_notfound_cid:
            raise ValueError(err_mesg)
        else:
            warnings.warn(err_mesg)

    chem_meta["is_validated"] = validated
    chem_meta["validation_details"] = validation_details

    return chem_meta
