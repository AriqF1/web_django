from ninja import Schema

class Kalkulator(Schema):
    nil1: int
    nil2: int
    opr: str
    hasil: int = 0

    def calcHasil(self):
        hasil = self.nil1 + self.nil2
        if self.opr == '-':
            hasil = self.nil1 - self.nil2
        elif self.opr == 'x':
            hasil = self.nil1 * self.nil2
        
        return {'nilai1': self.nil1, 'nilai2': self.nil2, 
                'operator': self.opr, 'hasil': self.hasil}
    
from pydantic import validator
import re

class Register(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 5:
            raise ValueError("Username harus lebih dari 3 karakter")
        return value
    
    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password harus lebih dari 8 karakter")
        
        pattern = r'^(?=.*[A-Za-z])(?=.*\d).+$'
        if not re.match(pattern, value):
            raise ValueError("Password harus mengandung huruf dan angka")
    