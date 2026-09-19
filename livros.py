def busca_livros(db):
    livros = db.execute("SELECT * FROM livros").fetchall()
    
    return livros

class Livro():
    def __init__(self, id, titulo, autor, ano, isbn, categoria, qtd):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.categoria = categoria
        self.qtd = qtd
        self.disponivel = True
        
    def esta_disponivel(self):
        return self.disponivel


