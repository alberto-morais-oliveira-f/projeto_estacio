import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


class GoogleDriveService:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = self.initialize_drive_service()

    def initialize_drive_service(self):
        """
        Inicializa o serviço Google Drive usando OAuth 2.0.
        :return: A instância de serviço do Google Drive.
        """
        # Tenta carregar credenciais do token.json
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # Se não há credenciais válidas, segue com o fluxo de autenticação
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Salva as credenciais para a próxima execução
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

        return build('drive', 'v3', credentials=self.creds)

    def list_files(self, page_size=10):
        """
        Lista os arquivos no Google Drive.
        :param page_size: O número de arquivos a listar.
        :return: Uma lista de arquivos com nomes e IDs.
        """
        try:
            results = self.service.files().list(
                pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return []
            else:
                print('Files:')
                for item in items:
                    print(f"{item['name']} ({item['id']})")
                return items
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def upload_file(self, file_name, file_path, mime_type):
        """
        Realiza o upload de um arquivo para o Google Drive.
        :param file_name: Nome do arquivo a ser salvo no Google Drive.
        :param file_path: Caminho do arquivo local.
        :param mime_type: Tipo MIME do arquivo.
        :return: O ID do arquivo carregado.
        """
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File ID: {file.get("id")}')
        return file.get('id')

    def delete_file(self, file_id):
        """
        Remove um arquivo do Google Drive.
        :param file_id: ID do arquivo a ser removido.
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f'File {file_id} deleted successfully')
        except HttpError as error:
            print(f"An error occurred: {error}")
