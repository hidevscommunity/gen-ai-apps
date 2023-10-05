import asyncio
from chain_functions import *
from utils.index_helper import *


def generate_index(user_doc_list, company_doc_list, w_client):
    user_index = create_index(user_doc_list, w_client, "User")
    company_index = create_index(company_doc_list, w_client, "Company") if len(company_doc_list) > 0 else None
    return user_index, company_index


def generate_sample_index(w_client):
    nodes_user = []
    for txt_path in [os.path.join("sample", "cv.txt"), os.path.join("sample", "personal_statement.txt")]:
        nodes = parse_doc(txt_path)
        nodes_user += nodes
    nodes_company = []
    for txt_path in [os.path.join("sample", "company_info_1.txt"), os.path.join("sample", "company_info_2.txt")]:
        nodes = parse_doc(txt_path)
        nodes_company += nodes
   
    vector_store_user = WeaviateVectorStore(weaviate_client=w_client, index_name="User", text_key="content")
    storage_context_user = StorageContext.from_defaults(vector_store = vector_store_user)
    user_index = VectorStoreIndex(nodes_user, storage_context=storage_context_user)

    vector_store_company = WeaviateVectorStore(weaviate_client=w_client, index_name="Company", text_key="content")
    storage_context_company = StorageContext.from_defaults(vector_store = vector_store_company)
    company_index = VectorStoreIndex(nodes_company, storage_context=storage_context_company)

    return user_index, company_index


def generation_pipeline(name, position, company, job_description, index_user, index_company=None):
    job_requirement, related_company_info = asyncio.run(generate_company_info_job_requirement(job_description, index_company))
    job_challenge = generate_role_challenge(position, job_description, related_company_info)
    first_paragraph = generate_first_paragraph(position, company, job_challenge, index_user)
    final_letter = generation_final_letter(name, position, company, job_requirement, first_paragraph, index_user)
    return final_letter
