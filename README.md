# Bike Rent Dashboard ✨
Sebuah analisis data penyewaan sepeda. Analisis ini dimulai dari gathering, assesing, cleaning, exploratory data anaysis, visualisation, dan dashboard. Pertanyaan analisis yang disajikan yaitu:
- Bagaimana tren penyewaan sepeda berdasarkan musimnya?
- Pada pukul berapa penyewaan sepeda paling tinggi?

# Setup environment anaconda
conda create --name main-ds python=3.9  
conda activate main-ds  
pip install -r requirements.txt  

# Setup Environment - Shell/Terminal  
mkdir Submission  
cd Submission  
pipenv install  
pipenv shell  
pip install -r requirements.txt  

# Run steamlit app  
streamlit run dashboard.py
