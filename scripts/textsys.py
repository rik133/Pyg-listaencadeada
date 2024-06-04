import pygame
from pygame.locals import *


class Text:
    """Create a text object."""

    def __init__(self, text, pos, fontsize = 14, game = None) :
        self.text = text
        self.pos = pos
        self.coisas = game.coisas
        self.fontname = None
        self.fontsize = fontsize
        self.fontcolor = Color('RED')
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        try:
            self.font = pygame.font.Font(('pygame-listaencadeada/fonts/'+ str(self.fontname)), self.fontsize)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, local):
        """Draw the text image to the screen."""
        local = self.coisas['dialogbox'][0]# Desenha a caixa de diálogo
        local.blit(self.img, (self.pos[0] + 10, self.pos[1] + 10))  # Desenha o texto na caixa de diálogo


class DialogNode:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.responses = []
    def checkfilho(self, tree):
        nodes = tree.node_dict 
        tree.current_node = self
        if  tree.current_node.id >= 0:
            paidemais = []    
            for _, childnode in nodes[tree.current_node.id].responses:
                paidemais.append(childnode)
                if paidemais.count(childnode)+1 > 1:
                    return True
    def add_response(self, response_text, next_node):
        
        self.responses.append((response_text, next_node))

class DialogTree:
    def __init__(self, root_node):
        self.root = root_node
        self.current_node = root_node
        self.node_dict = {root_node.id: root_node}

    def add_node(self, node):
        self.node_dict[node.id] = node

    def get_current_text(self):
        return self.current_node.text

    def get_responses(self):
        return self.current_node.responses

    def choose_response(self, response_index):
        if 0 <= response_index < len(self.current_node.responses):
            _, next_node = self.current_node.responses[response_index]
            self.current_node = next_node
        else:
            print("Resposta inválida")

    def reset(self):
        self.current_node = self.root

    def choose_node_by_id(self, node_id):
        if node_id in self.node_dict:
            self.current_node = self.node_dict[node_id]
        else:
            print("ID de nó inválido")
    def move_node(self, current_node_id, new_parent_node_id):
        current_node = None
        new_parent_node = None

        def find_node(node, node_id):
            if node.id == node_id:
                return node
            for response_text, child_node in node.responses:
                result = find_node(child_node, node_id)
                if result:
                    return result
            return None

        current_node = find_node(self.root, current_node_id)
        new_parent_node = find_node(self.root, new_parent_node_id)

        if not current_node or not new_parent_node:
            print("Nó não encontrado.")
            return

        def remove_node(node, target_node):
            for i, (response_text, child_node) in enumerate(node.responses):
                if child_node.id == target_node.id:
                    node.responses.pop(i)
                    return True
                if remove_node(child_node, target_node):
                    return True
            return False

        if self.root.id == current_node_id:
            print("Não é possível mover a raiz.")
            return

        if not remove_node(self.root, current_node):
            print("Erro ao remover o nó.")
            return

        new_parent_node.add_response(f"Movido para {new_parent_node.text}", current_node)
        print(f"Nó {current_node_id} movido para o pai {new_parent_node_id}")
    
                
             
   
def run_dialog(tree):
    while True:
        print(tree.get_current_text())
        responses = tree.get_responses()
        if not responses:
            break
        for i, resp in enumerate(responses):
            print(f"{i + 1}: {resp[0]}")
        choice = int(input("Escolha uma opção: ")) - 1
        tree.choose_response(choice)
        
def print_tree_pyramid(node, level=0):
    if level == 0:
        print(node.text)
    indent = ' ' * (4 * level)
    for response_text, child_node in node.responses:
        
        print(f"{indent}├── {response_text} -> {child_node.text}")
        if child_node.id < node.id:
            break
        else:
            print_tree_pyramid(child_node, level + 1)
def print_nodes(nodes):
    print("\nNodos existentes:")
    for node_id, node in nodes.items():
        print(f"ID: {node_id}, Texto: {node.text}")
# Código principal para manipular a árvore

def run_dialogtree():
    while True:
        print("\nOpções:")
        print("1. Adicionar nó")
        print("2. Adicionar resposta a um nó")
        print("3. Visualizar árvore de diálogo")
        print("4. Mover nó")
        print("5. Sair e retornar a árvore de diálogo")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            try: 
                node_id = int(input("Digite o ID do novo nó: "))
                node_text = input("Digite o texto do novo nó: ")
                new_node = DialogNode(node_id, node_text)
                tree.add_node(new_node)
                nodes[node_id] = new_node
            except ValueError: 
                print("ID inválido. Tente novamente.")
                
        elif choice == '2':
            try:
                node_id = int(input("Digite o ID do nó ao qual adicionar a resposta: "))
                if node_id in nodes:
                    response_text = input("Digite o texto da resposta: ")
                    next_node_id = int(input("Digite o ID do próximo nó: "))
                    if next_node_id in nodes:
                        if nodes[node_id].checkfilho(tree):
                            print("Não é possível adicionar um nó com dois pais.")
                        else: 
                            nodes[node_id].add_response(response_text, nodes[next_node_id])
                    else:
                        next_node_id = None
                        print("ID do próximo nó não encontrado.")
                else:
                    print("ID do nó não encontrado.")
            except ValueError:
                print("ID inválido. Tente novamente.")
        elif choice == '3':
            print("\nÁrvore de diálogo:")
            print_tree_pyramid(tree.root)
            print_nodes(nodes)
        elif choice == '4':
            try:
                current_node_id = int(input("Digite o ID do nó que deseja mover: "))
                new_parent_node_id = int(input("Digite o ID do novo pai: "))
                tree.move_node(current_node_id, new_parent_node_id)
            except ValueError:
                print("ID inválido. Tente novamente.")
        elif choice == '5':
            run_dialog(tree)
            break
        else:
            print("Opção inválida. Tente novamente.")
root_text = input("Digite o texto do nó raiz: ")
root_node = DialogNode(0, root_text)
tree = DialogTree(root_node)
nodes = {0: root_node} 
'''root = DialogNode(0,"Olá, aventureiro! O que você deseja saber?")
node1 = DialogNode(1,"Eu quero saber mais sobre esta cidade.")
node2 = DialogNode(2,"Eu estou procurando por uma missão.")
node3 = DialogNode(3,"Esta cidade é antiga e cheia de mistérios.")
node4 = DialogNode(4,"Há uma missão perigosa que precisa ser completada.")

root.add_response("Perguntar sobre a cidade", node1 )
root.add_response("Perguntar sobre missões", node2 )
node1.add_response("Ouvir mais sobre a cidade", node3 )
node2.add_response("Ouvir sobre a missão", node4 )
node3.add_response("Voltar ao início", root)
node4.add_response("Voltar ao início", root)

dialog_tree = DialogTree(root)
run_dialog(dialog_tree)'''

run_dialogtree()

