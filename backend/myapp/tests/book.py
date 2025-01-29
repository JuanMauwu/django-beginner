from django.test import TestCase
from rest_framework import status 
from django.urls import reverse
from myapp.models import Book


#TEST GET
class BookGetAPITest(TestCase): 
    def setUp(self):
        self.book1 = Book.objects.create(               #.objects es el manager usado en django para interactuar con la db, permite hacer consultas y operar con los registros de cada modelo propiamente
            title="The Catcher",                        #con el manager podemos usar operaciondes CRUD (Create, Read, Update, Delete) con los modelos. create() es uno de estos metodos
            author="J.D. Salinger",
            summary="A story about teenage rebellion.",
            pos_date="1951-07-16",
            active=True,
        )
        
        self.book2 = Book.objects.create(
            title="The",
            author="J.D.",
            summary="A story about teenage",
            pos_date="1951-07-14",
            active=True,
        )
        
        self.detail_url = reverse("myapp:book-list-create")
        self.response = self.client.get(self.detail_url)         #tener en cuenta que self.client se usa para simular un cliente web que interactua con la API  
        
    def test_status_code(self):
        #verificar si devuelve el codigo de estado correcto
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response_structure(self):
        data = self.response.json()
        
        #verificar si la data no esta vacia
        self.assertGreater(len(data), 0, "No data")        
        
        #verificar que los campos requeridos si esten en la respuesta
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertIn(field, data[0]) 
         
        #verificar que los campos requeridos si esten en la respuesta
        for field in expected_fields:                                    
            self.assertEqual(data[0][field], getattr(self.book1, field)) #funcion getattr, buscamos en este caso la clave field dentro de self.book1
    
        #verificar en db
        #para book1
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        book = Book.objects.get(id=self.book1.id)
        for field in expected_fields:
            if field == "pos_date":
                self.assertEqual(str(getattr(book, field)), getattr(self.book1, field))
            else:
                self.assertEqual(getattr(book, field), getattr(self.book1, field))

        #para book2
        book = Book.objects.get(id=self.book2.id)
        for field in expected_fields:
            if field == "pos_date":
                self.assertEqual(str(getattr(book, field)), getattr(self.book2, field))
            else:
                self.assertEqual(getattr(book, field), getattr(self.book2, field))
                
    def test_field_types(self):
        data = self.response.json()
       
        field_types = {
            "id":int,
            "title":str,
            "author":str,
            "summary":str,
            "pos_date":str,
            "active":bool,
        }

        #verificar que los tipos de campos de la respuesta sean los esperados
        for field, type in field_types.items():
            self.assertIsInstance(data[0][field], type)
            
#TEST GET DETAIL (detalles del Get)
class BookGetDetailApiTest(TestCase):
    def setUp(self):
        #crear el libro en la db de prueba
        self.book1 = Book.objects.create(
            title="The Catcher",
            author="J.D. Salinger",
            summary="A story about teenage rebellion.",
            pos_date="1951-07-16",
            active=True,            
        )
        
        self.detail_url = reverse("myapp:book-detail",kwargs = {"id": self.book1.id}) #obtiene/construye la URL para el endpoint y asi poderlo usar abajo
        self.response = self.client.get(self.detail_url, format="json") #hace la solicitud get al endpoint anteriormente conseguido
        
    def test_status_code(self):
        #verificar si devuelve el codigo de estado correcto
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        
    def test_response_structure(self):
        data = self.response.json()  #recordar que en caso de los detalles no devuelve una lista de dict, solo devuelve un dict
        
        #verificar que los campos requeridos si esten en la respuesta
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertIn(field, data)
        
        #verificar que los datos de la respuesta correspodan con el objeto creado para la prueba
        for field in expected_fields:
            self.assertEqual(data[field], getattr(self.book1, field))
        
        #comprobar en database
        #para book1
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        book = Book.objects.get(id=self.book1.id)
        for field in expected_fields:
            if field == "pos_date":
                self.assertEqual(str(getattr(book, field)), getattr(self.book1, field))
            else:
                self.assertEqual(getattr(book, field), getattr(self.book1, field))

        
    def test_field_type(self):
        data = self.response.json()
        
        #verificar que los tipos de campos de la respuesta sean los esperados
        field_types = {
            "id":int,
            "title":str,
            "author":str,
            "summary":str,
            "pos_date":str,
            "active":bool,
        }
        
        for field, type in field_types.items():  
            self.assertIsInstance(data[field], type) 
                    
#TEST POST
class BookPostAPITest(TestCase):
    def setUp(self):
        self.post_book_data = {
            "title": "El tunel",
            "author": "Pepito",
            "summary": "ooo",
            "pos_date": "2023-10-26",
            "active": True
        }
        
        self.url_book = reverse("myapp:book-list-create")
        self.response = self.client.post(self.url_book, self.post_book_data, format="json")

    def test_status_code(self):
        #verificar si devuelve el codigo de estado correcto
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
      
    def test_response_structure(self):
        data = self.response.json()
        
        #verificar que los campos requeridos si esten en la respuesta
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertIn(field, data)
        

        expected_fields = ["title", "author", "summary", "pos_date", "active"] #en estecaso no comparamos el id ya que no se encuentra en post book data
        # Compara los datos enviados con los datos devueltos
        for field in expected_fields:
            self.assertEqual(self.post_book_data[field], data[field])
        
        # Verifica que el libro ha sido creado en la base de datos
        expected_fields = ["title", "author", "summary", "pos_date", "active"]
        book = Book.objects.get(title=self.post_book_data["title"])
        
        for field in expected_fields:
            if field == "pos_date":  
                self.assertEqual(str(getattr(book, field)), self.post_book_data[field])
            else:
                self.assertEqual(getattr(book, field), self.post_book_data[field])
        
    def test_fields_types(self):
        data = self.response.json()
        # Verifica los tipos de datos
        
        field_types = {
            "id":int,
            "title":str,
            "author":str,
            "summary":str,
            "pos_date":str,
            "active":bool,
        }
        
        for field, type in field_types.items():
            self.assertIsInstance(data[field], type)
 
#TEST METODO DELETE       
class BookDeleteAPITest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="The Catcher",
            author="J.D. Salinger",
            summary="A story about teenage rebellion.",
            pos_date="1951-07-16",
            active=True,         
        )
        
        self.detail_url = reverse("myapp:book-detail", kwargs={"id":self.book1.id})
        self.response = self.client.delete(self.detail_url, format="json")
        
    def test_status_code(self):
        #verificar si devuelve el codigo de estado correcto
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_object_deleted(self):
        #verificar que el objeto no exista en la db
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
            
#METODO PUT (actualizar pero se deben pasar todos los campos)
class BookPutAPITest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="The Catcher",
            author="J.D. Salinger",
            summary="A story about teenage rebellion.",
            pos_date="1951-07-16",
            active=True, 
        )
        
        self.put_book_data = {
            "title":"The",
            "author":"J.D.",
            "summary":"A story",
            "pos_date":"2000-07-16",
            "active":False,            
        }
        
        self.detail_url = reverse("myapp:book-detail", kwargs={"id":self.book1.id})
        self.response = self.client.put(self.detail_url, self.put_book_data, content_type="application/json") #revisar(diferencia en content type)
        
    def test_status_code(self):
        #verificar si devuelve el codigo de estado correcto
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        
    def test_response_structure(self):
        data = self.response.json()

        #verificar que los campos requeridos si esten en la respuesta
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertIn(field, data)
        
        #verificar que los datos de la respuesta correspodan con la data de la solicitud
        expected_fields = ["title", "author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertEqual(data[field], self.put_book_data[field])
        
        #verificar que los datos del objeto en db correspondan con la data de la solicitud
        update_book = Book.objects.get(id=self.book1.id) #objects.get para oobtener un objeto de la db
        
        for field in expected_fields:
            if field == "pos_date":
                self.assertEqual(str(getattr(update_book, field)), self.put_book_data[field])
            else: 
                self.assertEqual(getattr(update_book, field), self.put_book_data[field])
        
    def test_field_types(self):
        data = self.response.json()
        
        field_types = {
            "id":int,
            "title":str,
            "author":str,
            "summary":str,
            "pos_date":str,
            "active":bool,
        }
        
        #verificar que los tipos de campos de la respuesta sean los esperados
        for field, type in field_types.items():
            self.assertIsInstance(data[field], type)

#TEST METODO PATCH (actualizar pero solo se pasa el campo a modificar, puede variar dado como esten definidos los campos en el modelo)
class BookPatchAPITest(TestCase):
    def setUp(self):
        
        self.post_book_data = {
            "title": "El tunel",
            "author": "Pepito",
            "summary": "ooo",
            "pos_date": "2023-10-26",
            "active": True            
        }
        
        self.patch_book_data = {         #se modificara el titulo
            "title": "El",               #segun el planteamiento del modelo es obligatorio poner la info para title, author y pos_date
            "author": "Pepito",
            "pos_date": "2023-10-26",            
        }
        
        #primero hacemos una solicitud post apra crear un libro en al db (otra forma)
        self.post_detail_url = reverse("myapp:book-list-create")
        self.post_response = self.client.post(self.post_detail_url, self.post_book_data, format="json")
        
        
        #segundo hacemos la solicitud del metodo patch con el objeto anteriormente creado
        self.detail_url = reverse("myapp:book-detail", kwargs={"id":self.post_response.json().get("id")}) #aqui usamos el metodo de los dic para obtener un valor o podemos usar #self.post_response.json()["id"]
        self.response = self.client.patch(self.detail_url, self.patch_book_data, content_type="application/json")
        
    def test_status_code(self):
        #verificar si devuelve el codigo de estado correcto
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        
    def test_response_structure(self):
        data = self.response.json()
        
        #verificar que los campos requeridos si esten en la respuesta
        expected_fields = ["id", "title", "author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertIn(field, data)
        
        #verificar que el cambio si se haya efectuado
        self.assertEqual(data["title"], self.patch_book_data["title"])
        
        #verificar que el resto de campos no se hayan modificado
        expected_fields = ["author", "summary", "pos_date", "active"]
        
        for field in expected_fields:
            self.assertEqual(data[field], self.post_book_data[field])
    
        #verificar que en la db se haya modificado el titulo correctamente        
        expected_fields = ["author", "summary", "pos_date", "active"]
        update_book = Book.objects.get(id=data["id"])

        self.assertEqual(update_book.title, self.patch_book_data["title"])
        
        #verificar que en la db el resto de datos no se hayan modificado
        for field in expected_fields:
            if field == "pos_date":
                self.assertEqual(str(getattr(update_book, field)), self.post_book_data[field])
            else:
                self.assertEqual(getattr(update_book, field), self.post_book_data[field])
        
    def test_fields_types(self):
        data = self.response.json()
        
        field_types = {
            "id":int,
            "title":str,
            "author":str,
            "summary":str,
            "pos_date":str,
            "active":bool,
        }
        
        #verificar que los tipos de campos de la respuesta sean los esperados
        for field, type in field_types.items():
            self.assertIsInstance(data[field], type)