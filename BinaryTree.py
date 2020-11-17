class Employee:
    # This class holds the sample data for the linked list read in from a csv file.
    # Importantly the data input function which reads the files and creates the lists is in this class and needs to be
    # recreated for any other data.
    def __init__(self, ID, Prefix, FirstName, MiddleInitial, LastName, Gender, Email):
        self.ID = ID
        self.Prefix = Prefix
        self.FirstName = FirstName
        self.MiddleInitial = MiddleInitial
        self.LastName = LastName
        self.Gender = Gender
        self.Email = Email

    def DataInput(self, FileName, EmployeeBinaryTree, EmployeeUnlinkedList):
        import csv
        with open(FileName, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for line in csv_reader:
                EmployeeBinaryTree.Insert(i, line[4])
                EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                i += 1


class LinkedListNode:
    def __init__(self, Value, Name):
        self.Value = Value
        self.Name = Name
        self.NextNode = None
        self.PreviousNode = None


class LinkedList:
    # This program uses a linked list for any clashes in ID for the binary tree
    def __init__(self):
        self.Head = None
        self.Tail = None

    def Insert(self, Value, Name):
        Node = LinkedListNode(Value, Name)
        if self.Head is None:
            self.Head = Node
        elif self.Tail is None:
            self.Tail = Node
            self.Tail.PreviousNode = self.Head
            self.Head.NextNode = Node
            Node.PreviousNode = self.Head
        else:
            self.Tail.NextNode = Node
            Node.PreviousNode = self.Tail
            self.Tail = Node

    def PrintLinkedList(self):
        CurrentNode = self.Head
        while CurrentNode != self.Tail:
            print (str(CurrentNode.Name) + " -> ")
            CurrentNode = CurrentNode.NextNode
        print(str(CurrentNode.Name))

    def FindEntryFromName(self, NodeName):
        CurrentNode = self.Head
        while CurrentNode.Name != NodeName and CurrentNode is not self.Tail:
            CurrentNode = CurrentNode.NextNode
        if CurrentNode.Name == NodeName:
            return CurrentNode.Value
        else:
            return 0

    def FindEntryFromPosition(self, NodePosition):
        CurrentNode = self.Head
        i = 0
        while i < NodePosition:
            CurrentNode = CurrentNode.NextNode
            i += 1
        return CurrentNode.Value

    def PresentEntries(self):
        CurrentNode = self.Head
        i = 1
        while CurrentNode != self.Tail:
            print("{}: {}".format(i, CurrentNode.Name))
            i += 1
            CurrentNode = CurrentNode.NextNode
        print("{}: {}".format(i, CurrentNode.Name))


class BinaryTreeNode:
    def __init__(self, Value, Name):
        self.Value = Value
        self.Name = Name
        self.HigherNode = None
        self.LowerNode = None
        self.Collided = False
        self.AssociatedLinkedList = None
        self.AssociatedUnlinkedList = None


class BinaryTree:
    def __init__(self):
        self.Head = None

    def NodeSort(self, Target, Subject):
        # Be aware this may throw a fault for data that cant use min() and will need a custom sort method
        # 0: same
        # 1: Subject is higher
        # 2: Target is higher
        if Target == Subject:
            return 0
        elif min(Target, Subject) == Target:
            return 1
        else:
            return 2

    def Insert(self, Value, Name):
        InsertNode = BinaryTreeNode(Value, Name)
        ComparisonNode = None
        IsPlaced = False
        if self.Head is None:
            self.Head = InsertNode
            IsPlaced = True
        else:
            ComparisonNode = self.Head
        while IsPlaced is False:
            if self.NodeSort(InsertNode.Name, ComparisonNode.Name) == 0: # Nodes are equal
                self.TreeCollision(InsertNode, ComparisonNode)
                IsPlaced = True
            elif self.NodeSort(InsertNode.Name, ComparisonNode.Name) == 1: # ComparisonNode is Higher
                if ComparisonNode.LowerNode is None:
                    ComparisonNode.LowerNode = InsertNode
                    IsPlaced = True
                else:
                    ComparisonNode = ComparisonNode.LowerNode
            elif self.NodeSort(InsertNode.Name, ComparisonNode.Name) == 2: # InsertNode is Higher
                if ComparisonNode.HigherNode is None:
                    ComparisonNode.HigherNode = InsertNode
                    IsPlaced = True
                else:
                    ComparisonNode = ComparisonNode.HigherNode

    def TreeCollision (self, TargetNode, SubjectNode):
        # This method resolves tree collisions caused by identical node names by forming a linked list of nodes
        # It checks whether a linked list already exists for this node
        # If it doesnt it creates one and inserts the subject node
        # Then it appends that list with the new entry
        # The node is inserted with a created name from its original name and its position eg Stevens (3) or Mark (0)
        # This is only its name within the linked list
        if not SubjectNode.Collided:
            SubjectNode.Collided = True
            CollisionLinkedList = LinkedList()
            CollisionUnlinkedList = []
            SubjectNode.AssociatedLinkedList = CollisionLinkedList
            SubjectNode.AssociatedUnlinkedList = CollisionUnlinkedList
            SubjectNode.AssociatedUnlinkedList.append(SubjectNode)
            LinkedListNodeName = (SubjectNode.Name + " ({})".format(len(SubjectNode.AssociatedUnlinkedList)))
            SubjectNode.AssociatedLinkedList.Insert(SubjectNode.Value, LinkedListNodeName)
        TargetNode.Collided = True
        TargetNode.AssociatedLinkedList = SubjectNode.AssociatedLinkedList
        TargetNode.AssociatedUnlinkedList = SubjectNode.AssociatedUnlinkedList
        TargetNode.AssociatedUnlinkedList.append(TargetNode)
        LinkedListNodeName = (TargetNode.Name + " ({})".format(len(TargetNode.AssociatedUnlinkedList)))
        TargetNode.AssociatedLinkedList.Insert(TargetNode.Value, LinkedListNodeName)

    def FindEntry(self, Name):
        ComparisonNode = self.Head
        while Name != ComparisonNode.Name:
            if self.NodeSort(Name, ComparisonNode.Name) == 1:
                ComparisonNode = ComparisonNode.LowerNode
            elif self.NodeSort(Name, ComparisonNode.Name) == 2:
                ComparisonNode = ComparisonNode.HigherNode
        if ComparisonNode.Collided:
            print("Multiple entries under {} found:".format(Name))
            ComparisonNode.AssociatedLinkedList.PresentEntries()
            UserChoice = input("Please choose number from above list: ")
            return ComparisonNode.AssociatedLinkedList.FindEntryFromPosition(int(UserChoice) - 1)
        else:
            return ComparisonNode.Value


ExampleEmployeeUnlinkedList = []
ExampleEmployeeBinaryTree = BinaryTree()
FileName = "EmployeeRecords.csv"
Employee.DataInput("", FileName, ExampleEmployeeBinaryTree, ExampleEmployeeUnlinkedList)
# this line allows you to retrieve the requested data
print(ExampleEmployeeUnlinkedList[ExampleEmployeeBinaryTree.FindEntry("Bumgarner")].ID)
