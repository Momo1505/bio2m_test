import os
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore")

def init_qa_system(pdf_dir="docs", db_dir="db"):
    loader = PyPDFDirectoryLoader(pdf_dir)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
    )

    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    vectorstore.persist()

    # Prompt généré par Claude
    prompt_template = """Tu es un assistant médical expert. Utilise UNIQUEMENT les informations du contexte fourni.

CONTEXTE MÉDICAL:
{context}

RÈGLES STRICTES:
1. Réponds UNIQUEMENT avec les informations du contexte
2. Si l'information n'est pas dans le contexte, dis exactement: "Cette information n'est pas disponible dans les documents fournis."
3. Utilise le vocabulaire médical précis du contexte
4. Cite les passages pertinents entre guillemets
5. Réponds en français médical professionnel

QUESTION: {question}

RÉPONSE MÉDICALE:"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    text_pipeline = pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.3",
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.2,
        device=0 if torch.cuda.is_available() else -1,
        return_full_text=False
    )

    llm = HuggingFacePipeline(pipeline=text_pipeline)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain

def ask_question(qa_chain, question):
    print(f"\n Question: {question}")
    print(" Recherche en cours...")

    try:
        result = qa_chain({"query": question})
        answer = result["result"]
        sources = result.get("source_documents", [])

        print(f" Réponse: {answer}")

        if sources:
            print(f"\n Sources trouvées ({len(sources)} documents):")
            for i, doc in enumerate(sources, 1):
                preview = doc.page_content
                print(f"  {i}. {preview}")

        return answer

    except Exception as e:
        error_msg = f" Erreur: {str(e)}"
        print(error_msg)
        return error_msg

def run_terminal():
    qa_chain = init_qa_system()

    while True:
        try:
            user_question = input("\n Votre question: ")
            if user_question.lower() in ['quit', 'quitter', 'exit', 'q']:
                print("Au revoir!")
                break
            if user_question.strip():
                ask_question(qa_chain, user_question)
            else:
                print("Veuillez poser une question")
        except KeyboardInterrupt:
            print("\n Au revoir!")
            break
        except Exception as e:
            print(f" Erreur: {e}")

    print("✅ Session terminée")


if __name__ == "__main__":
    run_terminal()