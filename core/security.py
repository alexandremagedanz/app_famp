import bcrypt

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função para verificar se a senha esta correta, comparando
    a senha em texto puro, informada pelo usuário, e o hash da
    senha que estará slvo no banco de dados durante a criação
    da conta.
    """
    senha_bytes = senha.encode('utf-8')
    hash_bytes = hash_senha.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes) # CRIPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha: str) -> str:
    """
    Função que gera e retorna o hash da senha.
    """
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8') 
