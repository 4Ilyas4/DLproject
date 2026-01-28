
Multimodal Search System for Industrial Spare Parts

During an industry-oriented project focused on spare parts identification for heavy machinery, I worked with a large, poorly structured legacy database containing technical drawings, images, and relational records. My primary responsibility was to analyze the existing data infrastructure, reconstruct implicit relationships between components, and assess the feasibility of machine learning approaches under real-world constraints.
This system provides image and text-based search for the JCB spare parts catalog. It was developed to modernize part retrieval through deep learning and semantic matching.

Core Features

* ETL pipeline migrated 100,000+ spare parts records from MS SQL Server to PostgreSQL.
* Legacy application reverse-engineering extracted and linked technical drawings to database records.
* Semantic keyword search utilizes VAE-generated embeddings for similarity matching.
* Vector retrieval is handled by FAISS for efficient similarity searches.
* Technical English-to-Russian translator fine-tuned on specialized data achieved a 91.4 ChrF score.
* R&D pipeline includes GANs for image stylization and SAM for automated component segmentation.

Technologies

* Frameworks: PyTorch, FastAPI.
* Models: VAE, GAN, SAM, CNN, Bi-LSTM.
* Database: MS SQL Server, PostgreSQL, FAISS.

Technical Metrics

* Autoencoder training reduced loss to approximately 0.64.
* Semantic matching achieved a cosine similarity of 0.80.
* Vector dimensions for search embeddings are set to 512.
