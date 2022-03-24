def empregados(ini):
    query = f"""
        SELECT id, nome, nascimento, sexo, cargo, salario, cadastro 
        FROM empregados LIMIT {ini}, 100;
    """
    return query
