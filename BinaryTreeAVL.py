from random import randint
class BinaryTree:
    def clear(self):
        self.setRoot(None)
        self.setRight(None)
        self.setLeft(None)
        self.setParent(None)
        self.setHeight()
        self.setAVL()
    def __init__(self, root = None):
        self.clear()
        self.setRoot(root)
    def insertMany(self, elements = []):
        for e in elements:
            self.insert(e)
    def getRoot(self):
        return self.root
    def setRoot(self, value):
        self.root = value
    def isEmpty(self):
        return self.root is None
    def isLeaf(self):
        return self.left is None and self.right is None
    def setLeft(self, tree):
        if isinstance(tree, BinaryTree) or tree is None :
            self.left = tree
            if tree is not None:
                tree.setParent(self)
    def setRight(self, tree):
        if isinstance(tree, BinaryTree) or tree is None :
            self.right = tree
            if tree is not None:
                tree.setParent(self)
    def setParent(self, tree):
        if isinstance(tree, BinaryTree) or tree is None :
            self.parent = tree
    def getRight(self):
        return self.right
    def getLeft(self):
        return self.left
    def getParent(self):
        return self.parent
    def getHeight(self):
        return self.height
    def setHeight(self):
        if self.isEmpty() :
            self.height = 0
        else:
            left, right = self.left, self.right
            if left : left.setHeight()
            if right : right.setHeight()
            leftHeight, rightHeight = 0 if left is None else left.getHeight(), 0 if right is None else right.getHeight()
            self.height = 1 + max(leftHeight, rightHeight)
    def setAVL(self):
        if self.isEmpty():
            self.avl = 0
        else:
            left, right = self.left, self.right
            if left : left.setAVL()
            if right : right.setAVL()
            leftHeight, rightHeight = 0 if left is None else left.getHeight(), 0 if right is None else right.getHeight()
            self.avl = rightHeight - leftHeight
    def getAVL(self):
        return self.avl
    def __str__(self):
        preorder, inorder = [], []
        self.preOrder(preorder)
        self.inOrder(inorder)
        return "BinTree("+str(list(map(str,preorder)))+", "+str(list(map(str,inorder)))+" )"
    def insert(self, value):
        if self.isEmpty():
            self.setRoot(value)
        else:
            root, left, right = self.getRoot(), self.left, self.right
            direction = value >= root
            treeToInsert = right if direction else left
            if treeToInsert is None:
                #Crear el nuevo arbol binario
                treeToInsert = BinaryTree()
                treeToInsert.insert(value)
                if direction:
                    self.setRight(treeToInsert)
                else:
                    self.setLeft(treeToInsert)
            else:
                treeToInsert.insert(value)
        self.setHeight()
        self.setAVL()
        if abs(self.getAVL()) > 1:
            self.balance(value)
        self.setHeight()
        self.setAVL()
        #return newRoot
    def search(self, value):
        if not self.isEmpty():
            if self.getRoot() == value:
                return self
            else:
                root, left, right = self.getRoot(), self.left, self.right
                direction = value > root
                treeToSearch = right if direction else left
                if treeToSearch is not None:
                    return treeToSearch.search(value)
        return None
    def maximum(self):
        current = self
        while current.getRight() is not None and not current.isEmpty():
            current = current.getRight()
        return current
    def minimum(self):
        current = self
        while current.getLeft() is not None and not current.isEmpty():
            current = current.getLeft()
        return current
    def preOrder(self, buffer = []):
        root, left, right = self.getRoot(), self.left, self.right
        if not self.isEmpty():
            buffer.append(root)
            if left:
                left.preOrder(buffer)
            if right:
                right.preOrder(buffer)
        return buffer
    def posOrder(self, buffer = []):
        root, left, right = self.getRoot(), self.left, self.right
        if not self.isEmpty():
            if left:
                left.posOrder(buffer)
            if right:
                right.posOrder(buffer)
            buffer.append(root)
        return buffer
    def inOrder(self, buffer = []):
        root, left, right = self.getRoot(), self.left, self.right
        if not self.isEmpty():
            if left:
                left.inOrder(buffer)
            buffer.append(root)
            if right:
                right.inOrder(buffer)
        return buffer
    def rotateLeft(self):
        #Rotar izquierda
        root, left, right, avl, rl = self.getRoot(), self.left, self.right, self.avl, self.right.getLeft()
        self.setRoot(right.getRoot())
        self.setRight(right.getRight())
        self.setLeft(BinaryTree(root))
        self.left.setRight(rl)
        self.left.setLeft(left)
        self.setHeight()
        self.setAVL()
    def rotateRight(self):
        #Rotar derecha
        root, left, right, avl, lr = self.getRoot(), self.left, self.right, self.avl, self.left.getRight()
        self.setRoot(left.getRoot())
        self.setLeft(left.getLeft())
        self.setRight(BinaryTree(root))
        self.right.setLeft(lr)
        self.right.setRight(right)
        self.setHeight()
        self.setAVL()
    def rotateLeftRight(self):
        root, left, right, avl = self.getRoot(), self.left, self.right, self.avl
        #
        lRoot, lvr, lvl, ll = left.getRoot(), left.right.right, left.right.left, left.left
        left.setRoot(left.right.getRoot())
        left.setLeft(BinaryTree(lRoot))
        left.setRight(lvr)
        left.left.setLeft(ll)
        left.left.setRight(lvl)
        self.rotateRight()
    def rotateRightLeft(self):
        root, left, right, avl = self.getRoot(), self.left, self.right, self.avl
        #
        rRoot, rr, lvr, lvl = right.getRoot(), right.right, right.left.right, right.left.left
        right.setRoot(right.left.getRoot())
        right.setRight(BinaryTree(rRoot))
        right.setLeft(lvl)
        right.right.setLeft(lvr)
        right.right.setRight(rr)
        self.rotateLeft()
    def balance(self, lastValue):
        root, left, right, avl = self.getRoot(), self.left, self.right, self.avl
        #Rotaciones de balance según criterios de AVL
        if avl > 1 and right.getRoot() <= lastValue:#Se encuentra desbalanceado por derecha y el último valor por derecha es menor o igual que la raiz
               self.rotateLeft()
        if avl > 1 and right.getRoot() > lastValue:  #Se encuentra desbalanceado por derecha
                self.rotateRightLeft()
        #Leftmost corner case
        if avl < -1 and left.getRoot() > lastValue: #Se encuentra desbalanceado por izquierda
                self.rotateRight()
        if avl < -1 and left.getRoot() <= lastValue: #Se encuentra desbalanceado por izquierda y el último valor por izquierda es menor o igual que la raiz
                self.rotateLeftRight()
        self.setHeight()
        self.setAVL()                       #Se revisa si se encuentra balanceado luego del cambio


    def delete(self, value):
        #Search v
        wrench= self.search(value)                  #Se busca si el valor se encuentra
        left, right, root = wrench.getLeft(), wrench.getRight(), wrench.getRoot()   #Se define la raiz, el subarbol izquierdo y subarbol derecho.
        if wrench is not None:
            # Se verifica si tiene más de un hijo
            has_two = wrench.getLeft() is not None and wrench.getRight() is not None
            #Bypass
            if not has_two:         #En caso de tener solo un hijo se realiza un corte
                parent = wrench.getParent()     #Se busca el antecesor del valor y luego se descenlaza de este
                wrench.clear()
                if left is not None: #Has left child
                    parent.setLeft(left)
                else: #Has right child
                    parent.setRight(right)
            #Find succesor          En caso de tener dos hijos, se debe encontrar un sucesor
            else:
                left_right_most = left.maximum()        #En esta solución será el mayor de los menores
                #Interchange succesor value with wrench value
                wrench.setRoot(left_right_most.getRoot())
                left_right_most.setRoot(root)
                parent = left_right_most.getParent()
                parent.setRight(None)
                left_right_most.clear()
                parent.setHeight()
                parent.setAVL()             #Y se calcula el AVL después del cambio
        else:
            raise Exception("No se encuentra el valor")
        self.setHeight()        #Se revisa la nueva altura para revisar si está balanceado
        self.setAVL()           #

    def update(self, old_key, new_key):
        self.delete(old_key)        #Se elimina el viejo valor
        self.insert(new_key)        #Se inserta el nuevo

def printTree(tree):
    pre, inO, pos = [], [], []
    tree.preOrder(pre)
    tree.inOrder(inO)
    tree.posOrder(pos)
    print("PreOrder", pre)
    print("InOrder", inO)
    print("PosOrder", pos)
    print("height", tree.getHeight())
    print("AVL Factor", tree.getAVL())


def main():
    rand = [i for i in range(10)]
    tree = BinaryTree()
    tree.insertMany(rand)
    for val in rand:
        t = tree.search(val)
    print("Arbol generado: ",tree, "Avl del árbol: ",tree.getAVL())
    tree.delete(5)
    print("Arbol generado luego de eliminar un valor: ", tree, "Avl del árbol luego del delete: ", tree.getAVL())
    tree.update(3, 29)
    print("Arbol generado luego de actualizar un valor: ", tree, "Avl del árbol luego del delete: ", tree.getAVL())

main()