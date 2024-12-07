
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from chat.features.handler_llama.base_llama import BaseLlama

class GenerateTextConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connessione WebSocket accettata.")

    async def disconnect(self, close_code):
        print("Connessione WebSocket chiusa.")
    
    async def receive(self, text_data):
        # Parsing del messaggio ricevuto dal frontend
        data = json.loads(text_data)
        prompt = data.get('prompt', 'Ciao!')
        print("Messaggio ricevuto:", prompt)  # Log il messaggio ricevuto

        base_llm = BaseLlama()
        model = base_llm.llm

        try:
            # Avvia lo streaming e applica il timeout manuale
            async for chunk_data in self.stream_text(model, prompt, max_tokens=100):
                print("Invio chunk:", chunk_data)  # Log del chunk inviato

                # Invio del chunk in un formato JSON semplificato e non ridondante
                await self.send(text_data=json.dumps({
                    'chunk': chunk_data['chunk'], #{'choices': [{'text': chunk_data['chunk']}]},
                    'done': chunk_data['done']
                }))
                
                await asyncio.sleep(0.1)  # Delay per l'effetto typing
        except asyncio.TimeoutError:
            await self.send(text_data=json.dumps({'error': 'Timeout: risposta troppo lenta'}))

    async def stream_text(self, model, prompt, max_tokens=100, timeout=30):
        start_time = asyncio.get_event_loop().time()
        loop = asyncio.get_event_loop()
        tokens_generated = 0  # Contatore per i token generati

        # Esegui la funzione modello in un executor per il threading, passando max_tokens
        chunk_generator = await loop.run_in_executor(None, self.run_model, model, prompt, max_tokens)

        try:
            while True:
                # Recupera il prossimo chunk dal generatore
                chunk = next(chunk_generator)
                
                # Controlla se il chunk è una stringa prima di usarlo
                if isinstance(chunk, str):
                    tokens_generated += len(chunk.split())
                else:
                    print("Il chunk non è una stringa:", chunk)
        
                current_time = asyncio.get_event_loop().time()
                if current_time - start_time > timeout:
                    raise asyncio.TimeoutError()
               
                # Verifica che il chunk non sia vuoto
                if chunk:
                    # Se il numero massimo di token è stato raggiunto, invia il chunk finale
                    if tokens_generated >= max_tokens:
                        yield {'chunk': chunk, 'done': True}  # Invio finale
                        break  # Interrompe lo streaming
                    else:
                        yield {'chunk': chunk, 'done': False}  # Invio normale
                else:
                    print("Chunk vuoto ricevuto, ignorando.")
   
        except StopIteration:
            # Gestione della fine del generatore
            print("Streaming completato.")
            # Forza invio di `done: true` alla fine dello streaming
            yield {'chunk': '', 'done': True}
        except Exception as e:
            print(f"Errore durante lo streaming del modello: {str(e)}")
            yield {'chunk': '', 'done': True}
            #await self.send(text_data=json.dumps({'error': str(e)}))

    def run_model(self, model, prompt, max_tokens):
        # Inizializza contatore di token
        tokens_generated = 0

        # Qui chiamiamo il modello e gestiamo lo streaming
        for chunk in model(prompt, max_tokens=max_tokens, stream=True, echo=False):
            # Accumula il testo del chunk e controlla i token
            print(chunk)
            yield chunk 
            """
            text_chunk = chunk['choices'][0]['text']
            tokens_generated += len(text_chunk.split())

            # Verifica il numero massimo di token
            if tokens_generated >= max_tokens:
                yield {'chunk': text_chunk, 'done': True}  # Ultimo invio
                break
            else:
                yield {'chunk': text_chunk, 'done': False}  # Invio normale
            """


class ProjectTreeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.project_tree = {}  # Initialize an empty project tree or load existing data
        print("WebSocket connection accepted for Project Tree.")

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")

    async def receive(self, text_data):
        # Parse the message received from the frontend
        data = json.loads(text_data)
        action = data.get('action')
        payload = data.get('payload')

        print("Received action:", action)

        if action == "expand_node":
            await self.handle_expand_node(payload)
        elif action == "add_project":
            await self.handle_add_project(payload)
        elif action == "update_activity":
            await self.handle_update_activity(payload)
        else:
            await self.send(text_data=json.dumps({'error': 'Unknown action'}))

    async def handle_expand_node(self, payload):
        node_id = payload.get('node_id')
        # Simulate loading more data for this node (e.g., fetch from DB)
        node_data = self.get_node_data(node_id)
        
        print(f"Expanding node {node_id}: {node_data}")
        await self.send(text_data=json.dumps({
            'action': 'expand_node',
            'node_id': node_id,
            'node_data': node_data
        }))

    async def handle_add_project(self, payload):
        project_name = payload.get('project_name')
        new_project = {"name": project_name, "activities": []}
        self.project_tree[project_name] = new_project

        print(f"Added new project: {new_project}")
        await self.send(text_data=json.dumps({
            'action': 'add_project',
            'project': new_project
        }))

    async def handle_update_activity(self, payload):
        project_name = payload.get('project_name')
        activity_name = payload.get('activity_name')
        update = payload.get('update')

        # Find and update the specified activity in the project tree
        if project_name in self.project_tree:
            project = self.project_tree[project_name]
            for activity in project['activities']:
                if activity['name'] == activity_name:
                    activity.update(update)

        print(f"Updated activity {activity_name} in project {project_name} with {update}")
        await self.send(text_data=json.dumps({
            'action': 'update_activity',
            'project_name': project_name,
            'activity_name': activity_name,
            'update': update
        }))

    def get_node_data(self, node_id):
        # Dummy data for example purposes; replace with database access or a more complex structure.
        return {
            "node_id": node_id,
            "name": f"Node {node_id}",
            "children": [
                {"id": f"{node_id}.1", "name": f"Child {node_id}.1"},
                {"id": f"{node_id}.2", "name": f"Child {node_id}.2"}
            ]
        }
