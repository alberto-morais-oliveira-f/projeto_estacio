import os
from tkinter import filedialog, messagebox

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


class GoogleDriveService:

    @staticmethod
    def create_folder_and_upload_file(client_name, filepath):
        """Cria uma pasta e faz o upload de um arquivo no Google Drive."""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Delete o arquivo token.json antes de rodar para resetar a autenticação
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        # Verifica se a pasta já existe
        query = f"name = '{client_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name)', pageSize=10).execute()
        items = results.get('files', [])

        if len(items) > 0:
            # Usa a primeira pasta encontrada com o nome correspondente
            folder_id = items[0]['id']
        else:
            # Cria uma pasta no Google Drive
            folder_metadata = {
                'name': client_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = folder.get('id')

        # Envia um arquivo para a pasta criada no Google Drive
        file_metadata = {
            'name': os.path.basename(filepath),
            'parents': [folder_id]
        }
        media = MediaFileUpload(filepath, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')

    def select_and_upload_file(self, client_name):
        initial_directory = "/home/alberto/Documentos"
        filepath = filedialog.askopenfilename(initialdir=initial_directory)
        if filepath:
            file_id = self.create_folder_and_upload_file(client_name, filepath)
            messagebox.showinfo("Success", f"Arquivo carregado com sucesso na pasta '{client_name}'! (ID: {file_id})")
        else:
            messagebox.showwarning("Atenção", "Nenhum arquivo selecionado")
