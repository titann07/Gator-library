import sys
import time

class Node1:
    def __init__(self, book_id, book_name, author_name, availability_status, borrowed_by, reservation_heap):
     # Initializing the Node, which is a representation of a book in the library, along with its attributes and status.
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = borrowed_by
        self.reservation_heap = reservation_heap
        self.color = 'black'
        self.parent = None
        self.left = None
        self.right = None

    
    def __repr__(self):
    # Provide a string representation of the node, detailing its key attributes.
        if self.book_id is None:
            return "NIL Node"
        return (f"Node(book_id={self.book_id}, book_name='{self.book_name}', "
                f"author_name='{self.author_name}', availability_status={self.availability_status}, "
                f"borrowed_by={self.borrowed_by}, reservations={list(self.reservation_heap.heap)})")
class MinHeap:
    def __init__(self):
        # Initializaion of an empty heap.
        self.heap = []

    def insert(self, z):
         # Insert an element, the heap and maintain the min-heap property.
        self.heap.append(z)
        self.bubbleup(len(self.heap) - 1)

    def extract_min(self):
        # Remove, return the smallest element from heap.
        if not self.heap:
            raise IndexError("Extracting from an empty heap is not allowed.")
        min_val = self.heap[0]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            self.heapify(0)
        else:
            self.heap.pop()
        return min_val

    def heapify(self, index):
        # Helper method to maintain the min-heap property 
        smallest = index
        Leftchild = 2 * index + 1
        Rightchild = 2 * index + 2

        if Leftchild < len(self.heap) and self.heap[Leftchild] < self.heap[smallest]:
            smallest = Leftchild

        if Rightchild < len(self.heap) and self.heap[Rightchild] < self.heap[smallest]:
            smallest = Rightchild

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify(smallest)

    def bubbleup(self, index):
        # Helper method to adjust the heap upwards.
        parentindex = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parentindex]:
            self.heap[index], self.heap[parentindex] = self.heap[parentindex], self.heap[index]
            self.bubbleup(parentindex)

class RedBTree:
    def __init__(self):
        # Initialize RedBlackTree with a NIL node as root, set its color to black.
        self.NIL = Node1(None, None, None, None, None, MinHeap())
        self.NIL.color = 'black'
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL
        self.insert_fixup_count = 0
        
    def min(self, n):
        # Finding node with the minimum value in the subtree.
            while n.left != self.NIL:
                n = n.left
            return n
        
    
    def trans(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def delete(self, z):
        # Delete a node z from the Red-Black Tree and maintain its properties.
        
            if z is None or z == self.NIL:
                return  # Ensure we're not trying to delete a None or NIL node
            
            y = z
            y_original_color = y.color
            if z.left == self.NIL:
                x = z.right
                if x != self.NIL:  # Check if x is not NIL before transplant
                    self.trans(z, z.right)
            elif z.right == self.NIL:
                x = z.left
                if x != self.NIL:  # Check if x is not NIL before transplant
                    self.trans(z, z.left)
            else:
                y = self.min(z.right)
                y_original_color = y.color
                x = y.right
                if y.parent == z:
                    x.parent = y
                else:
                    self.trans(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self.trans(z, y)
                y.left = z.left
                y.left.parent = y
                y.color = z.color
                if x != self.NIL:  # Check if x is not NIL before setting parent
                    x.parent = y
            if y_original_color == 'black':
                self.delete_fixup(x if x != self.NIL else self.root)
        
    
    
    def delete_fixup(self, x):
        # Adjust the tree after deletion to maintain Red-Black Tree properties.
        
            while x != self.root and x.color == 'black':
                if x == x.parent.left:
                    w = x.parent.right
                    if w and w.color == 'red':
                        # Perform color flips and rotations to rebalance the tree.
                        self.flip_color(w)  # Color flip
                        self.flip_color(x.parent)  # Color flip
                        self.leftrotate(x.parent)
                        w = x.parent.right
                    if w and w.left.color == 'black' and w.right.color == 'black':
                        w.color = 'red'  # Color flip
                        if w.color != 'red':
                            self.insert_fixup_count += 1  # Count the color flip
                        x = x.parent
                    else:
                        if w and w.right.color == 'black':
                            w.left.color = 'black'  # Color flip (although it's already black)
                            w.color = 'red'  # Color flip
                            if w.left.color != 'black' or w.color != 'red':
                                self.insert_fixup_count += 1  # Count the color flip
                            self.rightrotate(w)
                            w = x.parent.right
                        w.color = x.parent.color
                        x.parent.color = 'black'  # Color flip
                        w.right.color = 'black'  # Color flip (although it's already black)
                        if w.color != x.parent.color or x.parent.color != 'black' or w.right.color != 'black':
                            self.insert_fixup_count += 2  # Count the color flips
                        self.leftrotate(x.parent)
                        x = self.root
                else:
                    # Similar logic for the right side
                    ...
            x.color = 'black'  # Color flip (if x is not already black)
            if x.color != 'black':
                self.flip_color(x)  # Count the color flip
        
    
    def flip_color(self, node):
        # Flip the color of a node and increment the fixup counter.
        
            if node.color == 'black':
                node.color = 'red'
            else:
                node.color = 'black'
            self.insert_fixup_count += 1
        


    def insert(self, node):
        # Insert a node into the Red-Black Tree and fix the tree to maintain its properties.
            print(f'Inserting node with book_id: {node.book_id}')
            y = None
            x = self.root
            while x != self.NIL:
                y = x
                if node.book_id < x.book_id:
                    x = x.left
                else:
                    x = x.right
            node.parent = y
            if y is None:
                self.root = node
            elif node.book_id < y.book_id:
                y.left = node
            else:
                y.right = node
            node.left = self.NIL
            node.right = self.NIL
            node.color = 'red'
            self.fix_insert(node)
            print(f'Node with book_id: {node.book_id} inserted')
        

    def fix_insert(self, node):
        # Fix the tree after insertion to maintain Red-Black Tree properties.
            print(f'Fixing insert for node with book_id: {node.book_id}')
            while node != self.root and node.parent and node.parent.color == 'red':
                uncle = None
                if node.parent == node.parent.parent.left:
                    uncle = node.parent.parent.right
                    if uncle.color == 'red':
                        node.parent.color = 'black'
                        uncle.color = 'black'
                        node.parent.parent.color = 'red'
                        self.insert_fixup_count += 3  #the no. color flips
                        #self.insert_fixup_count += 1
                        node = node.parent.parent
                        
                    else:
                        if node == node.parent.right:
                            node = node.parent
                            self.leftrotate(node)
                        node.parent.color = 'black'
                        node.parent.parent.color = 'red'
                        self.rightrotate(node.parent.parent)
                        self.insert_fixup_count += 2  # the no. color flips
                else:
                    uncle = node.parent.parent.left
                    if uncle.color == 'red':
                        node.parent.color = 'black'
                        uncle.color = 'black'
                        node.parent.parent.color = 'red'
                        self.insert_fixup_count += 3  # the no. color flips
                        node = node.parent.parent
                    else:
                        if node == node.parent.left:
                            node = node.parent
                            self.rightrotate(node)
                        node.parent.color = 'black'
                        node.parent.parent.color = 'red'
                        self.leftrotate(node.parent.parent)
                        self.insert_fixup_count += 2  # Count the color flips
            self.root.color = 'black'
            print(f'Insert fix complete for node with book_id: {node.book_id}')
            if self.root.color == 'red':
                self.insert_fixup_count += 1  # Count the color flip if root changes to black'
        

    def leftrotate(self, x):
        # Perform a left rotation around a given node.
            if x is None or x.right is None:
                return "Error: 'None' node found in leftrotate"

            y = x.right
            x.right = y.left
            if y.left is not None:
                y.left.parent = x

            y.parent = x.parent
            if x.parent is None:
                self.root = y
            elif x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

            y.left = x
            x.parent = y
            return "leftrotate execution is successfull"
        

    def rightrotate(self, y):
        # Perform a right rotation around a given node.

            if y is None or y.left is None:
                return "Error: 'None' node found in rightrotate"

            x = y.left
            y.left = x.right
            if x.right is not None:
                x.right.parent = y

            x.parent = y.parent
            if y.parent is None:
                self.root = x
            elif y == y.parent.right:
                y.parent.right = x
            else:
                y.parent.left = x

            x.right = y
            y.parent = x
            return "rightrotate executed successfully"
        

    
    def print_books_range(self, book_id1, book_id2):
        # Print details of books in a specified range of IDs.
        booklist = []
        self._print_books_range(self.root, book_id1, book_id2, booklist)
        return booklist
    
    def _print_books_range(self, node, book_id1, book_id2, booklist):
        # Helper method to traverse the tree and collect book details in specified range.

            if node is not None and node != self.NIL:
                if book_id1 < node.book_id:
                    self._print_books_range(node.left, book_id1, book_id2, booklist)
                if book_id1 <= node.book_id <= book_id2:
                    # Extract only the patron IDs from reservations heap
                    reservations = [str(res[2]) for res in node.reservation_heap.heap] if node.reservation_heap.heap else []
                    # Format details as a multi-line string
                    book_details = (
                        f"BookID = {node.book_id}\n"
                        f"Title = \"{node.book_name}\"\n"
                        f"Author = \"{node.author_name}\"\n"
                        f"Availability = {'Yes' if node.availability_status else 'No'}\n"
                        f"BorrowedBy = {node.borrowed_by if node.borrowed_by else 'None'}\n"
                        f"Reservations = [{', '.join(reservations)}]\n"
                    )
                    booklist.append(book_details)
                if book_id2 > node.book_id:
                    self._print_books_range(node.right, book_id1, book_id2, booklist)
        


    def search(self, node, book_id):
         # Search for books by their ID in the tree.
            if node is None or node == self.NIL or book_id == node.book_id:
                return node
            if book_id < node.book_id:
                return self.search(node.left, book_id)
            else:
                return self.search(node.right, book_id)
        


class GatorLibrary:

    def __init__(self):
        # Initialize the library with a Red-Black Tree to store book data and a counter for color flips.
        self.rb_tree = RedBTree()
        self.color_flip_count = 0  # To keep track of color flip counts during insertions
    def colorflip(self):
        self.color_flip_count += 1
        
    def filecommands(self, input_filename):
         # Read and return a list of commands from the specified input file.
            with open(input_filename, 'r') as file:
                commands = file.readlines()
            return commands


    def outputtofile(self, output_filename, output_lines):
        # Write given output lines to the specified output file.
        with open(output_filename, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')

    def run(self, command):
         # Parse and execute a given command string, handling various library operations.
        
        try:
            parts = command.strip().replace(')', '(').split('(')
            cmd_type = parts[0].strip()
            args = [arg.strip().strip('"') for arg in parts[1].split(',') if arg]

            if cmd_type == 'InsertBook':
                args = parts[1].split(',', 3) 
                args = [arg.strip().strip('"') for arg in args]
                try:
                    book_id = int(args[0])
                    book_name = args[1]
                    author_name = args[2]
                    availability_status = args[3] == 'Yes'
                except (ValueError, IndexError) as e:
                    return f"Error(InsertBook arguments): {e}", True
                return self.insert_book(book_id, book_name, author_name, availability_status), True

            elif cmd_type == 'PrintBook':
                book_id = int(args[0])
                return self.print_book(book_id), True
            
            elif cmd_type == 'BorrowBook':
                patron_id = int(args[0])
                book_id = int(args[1])
                patron_priority = int(args[2])
                return self.borrow_book(patron_id, book_id, patron_priority), True
            
            elif cmd_type == 'PrintBooks':
                
                
                book_id1 = int(args[0].strip())
                book_id2 = int(args[1].strip())
                return self.print_books(book_id1, book_id2), True

            elif cmd_type == 'ReturnBook':
                # Make sure command is split properly
                args = [arg.strip().strip('"') for arg in parts[1].split(',')]
                if len(args) < 2:
                    return "Error: Not enough arguments for ReturnBook", True
                try:
                    patron_id = int(args[0].strip())
                    book_id = int(args[1].strip())
                except ValueError as e:
                    return f"Error in ReturnBook arguments: {e}", True
                return self.return_book(patron_id, book_id), True
                
            elif cmd_type == 'FindClosestBook':
                target_str = command.split('(')[1].split(')')[0].strip()
                # Check if the '(' and ')' are present and properly formatted
                try:
                    # Extract the number within the parentheses
                    target = int(target_str)
                    # Attempt to convert the string to an integer
                    target = int(target_str)
                except (ValueError, IndexError) as e:
                    return f"Error parsing target ID for FindClosestBook: {e}", True

                return self.find_closest_book(target), True
                
            elif cmd_type == 'DeleteBook':
                book_id = int(args[0])
                # return book_id
                return self.delete_book(book_id), True
                
            elif cmd_type == 'ColorFlipCount':
                return f"Colour Flip Count: {self.color_flip_count}", True
                
            elif cmd_type == 'Quit':
                return "Program Terminated!!", False  # Signal to stop command execution
            else:
                return f"Unknown command: {cmd_type}", True  # Continue command execution with result
        
        except Exception as e:
            return f"", True  # Continue command execution with error message



    def insert_book(self, book_id, book_name, author_name, availability_status):
        
            # Insert book into the Tree
            new_book = Node1(book_id, book_name, author_name, availability_status, None, MinHeap())
            self.rb_tree.insert(new_book)
            self.color_flip_count += self.rb_tree.insert_fixup_count  # Update color flip count
            self.rb_tree.insert_fixup_count = 0  # reset the fix-up count after the operation
            return ""
        
    

    def print_book(self, book_id):
            # Print details of the book with the given book_id
            node = self.rb_tree.search(self.rb_tree.root, book_id)
            if node and node != self.rb_tree.NIL:
                reservations = [str(reservation[2]) for reservation in node.reservation_heap.heap]  # Extract patron IDs
                formatted_reservations = f"[{', '.join(reservations)}]" if reservations else "[]"
                book_details = [
                    f"BookID = {node.book_id}",
                    f"Title = \"{node.book_name}\"",
                    f"Author = \"{node.author_name}\"",
                    f"Availability = {'Yes' if node.availability_status else 'Noo'}",
                    f"BorrowedBy = {node.borrowed_by if node.borrowed_by else 'Noonee'}",
                    f"Reservations = {formatted_reservations}\n"  # Use the adjusted reservations list
                ]
                return '\n'.join(book_details)
            else:
                return "BookID is not found in Library\n"
       
        
    def print_books(self, book_id1, book_id2):
        # This method will call a method on the RBTree to print the details
        # of all books within the given range.
        if book_id1 > book_id2:
            return "Invalid range\n"

        # Call the helper function on the RBTree with the provided range
        booklist = self.rb_tree.print_books_range(book_id1, book_id2)

        # Convert the list of book details into a formatted string
        output_str = "\n".join(booklist)
        print(output_str)
        return output_str


    def borrow_book(self, patron_id, book_id, patron_priority):
        node = self.rb_tree.search(self.rb_tree.root, book_id)
        if not node:
            return "BookID not found \n"

        # Check if the book is already borrowed by the same patron
        if node.borrowed_by == patron_id:
            return f"Book {book_id} Already Borrowed by Patron {patron_id}\n"

        # Check if the book is available for borrowing
        if node.availability_status:
            node.availability_status = False
            node.borrowed_by = patron_id
            return f"Book {book_id} Borrowed by Patron {patron_id}\n"

        # Check reservation limit
        if len(node.reservation_heap.heap) >= 20:
            return f"Unable to reserve book {book_id} for Patron {patron_id}; reservation limit reached.\n"

        # Add patron to the reservation heap
        timestamp = time.time()  # Use timestamp for FIFO order among same-priority reservations
        node.reservation_heap.insert((patron_priority, timestamp, patron_id))
        return f"Book {book_id} Reserved by Patron {patron_id}\n"
        

    def return_book(self, patron_id, book_id):
        node = self.rb_tree.search(self.rb_tree.root, book_id)
        if not node or node == self.rb_tree.NIL:
            return "BookID not found \n"

        # Check if the book is currently borrowed by the given patron
        if not node.availability_status and node.borrowed_by == patron_id:
            # Process the next reservation, if any
            if node.reservation_heap.heap:
                next_patron_info = node.reservation_heap.extract_min()
                next_patron = next_patron_info[2]
                node.borrowed_by = next_patron
                return f"Book {book_id} returned by Patron {patron_id}\nBook {book_id} allotted to Patron {next_patron}.\n"
            else:
                # Make the book available if there are no reservations
                node.availability_status = True
                node.borrowed_by = None
                return f"Book {book_id} returned by Patron {patron_id} and is now available.\n"
        else:
            return "Return operation failed. Either the book is not borrowed or it is borrowed by another patron.\n"
        

            
    def find_closest_book(self, target):
        closest_books = self._find_closest_book(self.rb_tree.root, target, [])
        if closest_books:
            closest_books.sort(key=lambda book: book.book_id)
            return "\n".join([self.print_book(book.book_id) for book in closest_books])
        else:
            return "No books available \n"
        

    def _find_closest_book(self, node, target, closest_books):
        
        if node is None or node == self.rb_tree.NIL:
            return closest_books

        if not closest_books:
            closest_books.append(node)
        else:
            current_distance = abs(target - node.book_id)
            closest_distance = abs(target - closest_books[0].book_id)

            if current_distance < closest_distance:
                closest_books = [node]
            elif current_distance == closest_distance:
                closest_books.append(node)

        if node.book_id < target:
            # Check right subtree
            closest_books = self._find_closest_book(node.right, target, closest_books)
        else:
            # Check left subtree
            closest_books = self._find_closest_book(node.left, target, closest_books)

        return closest_books

    
    
    def delete_book(self, book_id):
        node = self.rb_tree.search(self.rb_tree.root, book_id)
        if node is not None and node != self.rb_tree.NIL:
            # Notify patrons if  active reservations
            if node.reservation_heap.heap:
                patrons_to_notify = [str(heap_node[2]) for heap_node in node.reservation_heap.heap]
                node.reservation_heap.heap = []  # Clear reservations
                self.rb_tree.delete(node)
                self.color_flip_count += self.rb_tree.insert_fixup_count
                self.rb_tree.insert_fixup_count = 0  # Reset the fix-up count
                return f"Book {book_id} is no longer available. Reservations made by Patrons {','.join(patrons_to_notify)} have been cancelled!\n"
            
            else:
                # Delete the book if no reservations
                self.rb_tree.delete(node)
                self.color_flip_count += self.rb_tree.insert_fixup_count
                self.rb_tree.insert_fixup_count = 0  
                return f"Book {book_id} is no longer available.\n"
        else:
            return "BookID not found in the Library.\n"
    


    # FileHandling
    def filecommands(self, input_filename):
        try:
            with open(input_filename, 'r', encoding='utf-8') as file:
                commands = file.readlines()
            return commands
        except IOError as e:
            print(f"Fail to read file {input_filename}: {e}")
            return []

    def outputtofile(self, output_filename, output_lines):
        with open(output_filename, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')


# usage of the classes to create a library system
if __name__ == "__main__":
    import sys

    # Check if the correct number of arguments is given
    if len(sys.argv) != 2:
        print("Usage: python gator_library.py <input_filename>")
        sys.exit(1)

    # Get the input filename from command line argument
    input_filename = sys.argv[1]
    # Determine the output filename based on the input filename
    output_filename = input_filename.split('.')[0] + "_output_file.txt"
    
    # Instantiate the library system
    library_system = GatorLibrary()

    # Read commands from the input file
    commands = library_system.filecommands(input_filename)
    output_lines = []

    # Execute command and collect the Fresults
    for command in commands:
        result, continue_execution = library_system.run(command.strip())
        if not continue_execution:
            output_lines.append(result)
            break
        output_lines.append(result)

    # Write results to output file
    library_system.outputtofile(output_filename, output_lines)
    print(f"Output written to {output_filename}")