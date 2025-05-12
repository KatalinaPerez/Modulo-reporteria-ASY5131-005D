Antes de comenzar, asegúrate de tener instalado:

- Python 3.10 o superior
- Git (opcional, si clonas el proyecto)
- Acceso a un token de Doppler 
    (dp.st.dev WPEYWCAnvo5UPzxgfNB273CbuFwWr4jSrw5JScBe3MR)

2️⃣Un buen paso es crear un entorno virtual. Esto debe ser dentro da la carpeta de tu proyecto:

python -m venv .venv
.venv\Scripts\Activate.ps1

3️⃣ Instala las dependencias
pip install -r requirements.txt

4️⃣ Instala Doppler CLI, esto debido a que no se puede descargar desde requeriments.txt
 iwr -useb https://cli.doppler.com/install/windows | iex
 winget install --id Doppler.doppler

5️⃣ Configura tu token de Doppler
$env:DOPPLER_TOKEN="dp.st.el_token"
