import argparse
from app.core.rag.rag_pipeline import RAG_Pipeline

def main():
    parser = argparse.ArgumentParser(description='Run RAG_Pipeline')
    parser.add_argument('--basename', type=str, help="Knowledge Base Name")
    parser.add_argument('--new_basename', type=str, help="New Knowledge Base Name")
    parser.add_argument('--baseid', type=str, help="Knowledge Base ID")
    parser.add_argument('--file', type=str, help="File Path")
    parser.add_argument('--q', type=str, help="Question")
    
    # Define position argument for operation
    parser.add_argument('operation', choices=['create', 'modify', 'delete', 'insert', 'answer', 'retriever'],
                        help='Operation to perform')

    args = parser.parse_args()

    rag_pipeline = RAG_Pipeline()
    if args.operation == 'create':
        print("Create Knowledge Base")
        rag_pipeline.create_knowledgebase(args.basename)
    elif args.operation == 'modify':
        print("Modify Knowledge Base")
        rag_pipeline.modify_knowledgebase(args.new_basename, args.baseid)
    elif args.operation == 'delete':
        print("Delete Knowledge Base")
        rag_pipeline.delete_knowledgebase(args.basename)
    elif args.operation == 'insert':
        print("Insert Knowledge Base")
        rag_pipeline.insert_knowledgebase(args.file, args.baseid)
    elif args.operation == 'answer':
        print("Answer Question")
        answer = rag_pipeline.generate_answer_by_knowledgebase(args.q, args.baseid)
        print(answer)
    elif args.operation == 'retriever':
        print("Retriever Question")
        # Assuming there's a method for retrieval
        source_docs = rag_pipeline.retriever_by_knowledgebase(args.q, args.baseid)
        prompt_source = ""
        
        for source in source_docs:
            prompt_source += f"""
            {source.content}\n
            """
        print(prompt_source)

if __name__ == '__main__':
    main()