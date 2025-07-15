import pytest
import requests

class Constants:
    API_URL = "https://check-dev.g5dl.com/api/v1/"
    EMAIL = "oukb1147@gmail.com"
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbWwtYmFja2VuZC1nYXRld2F5Iiwic3ViIjoiMDE5MDEwYjQtYTVmZS03MmYzLTllYjUtM2E4NDg2YjY1ODY1IiwiYXVkIjpbImFtbC1iYWNrZW5kLWdhdGV3YXktdXNlcnMiXSwiZXhwIjoxNzUyNjY4NzIyLCJuYmYiOjE3NTI1ODIzMjIsImlhdCI6MTc1MjU4MjMyMiwiZmluZ2VycHJpbnQiOiJJTTA4Z1NyK3FhbnJDVkhMc2FnV1RBbnoxVlZ4NFVTVmxibDBnT2M2cldNPSIsInVzZXJfcm9sZSI6M30.L2vOdJOdfFRjWl8NWENsg43OENho-LuVk-K4kyVhBVI"
    REFRESH_TOKEN = "01980e0b-140b-7549-816a-ed8ff8e4d924"
