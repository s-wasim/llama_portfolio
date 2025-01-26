from sentence_transformers import SentenceTransformer
import os

def setup_embedding_models():
    # Define model name and cache path
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    cache_dir = os.path.join(os.getcwd(), 'model_cache')
    
    # Create cache directory
    os.makedirs(cache_dir, exist_ok=True)
    
    try:
        # Download and cache model
        model = SentenceTransformer(model_name, cache_folder=cache_dir)
        print(f"Model successfully downloaded to: {cache_dir}")
        return True
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

if __name__ == "__main__":
    setup_embedding_models()