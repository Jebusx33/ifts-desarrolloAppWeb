class Libro(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(255))
    imagen = mysql.Column(mysql.String(255))
    url = mysql.Column(mysql.String(255))
