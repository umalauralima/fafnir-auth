# 1. Imagem base com Python 3.12
FROM python:3.12-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia apenas os arquivos de dependências primeiro (para cache)
COPY requirements.txt .

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o código do projeto
COPY . .

# 6. Expõe a porta que o Flask vai usar
EXPOSE 5000

# 7. Variável de ambiente para o Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# 8. Comando para rodar a aplicação
CMD ["flask", "run"]