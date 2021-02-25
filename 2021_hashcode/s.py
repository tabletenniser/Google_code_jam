import numpy
import sys

class Solution(object):
    def __init__(self, books, libraries, lib_books, d):
        self.books = books
        self.libraries = libraries
        self.lib_books = lib_books
        self.d = d
        self.scanned_books = set()

    def get_lib_score(self, lib_with_ind):
        lib_index, library = lib_with_ind
        books_can_be_scanned = (int(self.d/2)-library[1]) * library[2]
        sorted_books = self.get_books(self.lib_books[lib_index], library)
        score = 0
        for b_ind in sorted_books[:books_can_be_scanned]:
            score += self.books[b_ind]
        return score

    def get_books(self, lib_books, library):
        books_to_scan = list(set(lib_books) - self.scanned_books)
        return sorted(books_to_scan, key=lambda x:self.books[x], reverse=True)

    def get_opt_solution(self):
        solution = []
        num_lib_selected = 0
        # self.sorted_book_index = numpy.argsort(self.books)[::-1]
        libs_with_index_and_score = list(zip(list(enumerate(self.libraries)), [self.get_lib_score(lib_with_ind) for lib_with_ind in enumerate(self.libraries)]))
        # print(libs_with_index_and_score)
        sorted_libs_with_index = [e[0] for e in sorted(list(libs_with_index_and_score), key=lambda x:x[1])]
        # print(sorted_libs_with_index)
        days_left = self.d
        for lib_with_ind in sorted_libs_with_index:
            lib_index, library = lib_with_ind
            sorted_books = self.get_books(self.lib_books[lib_index], library)
            num_books_can_be_scanned = days_left * library[2]
            sorted_books = sorted_books[:num_books_can_be_scanned]
            if len(sorted_books) > 0:
                days_left -= library[1]
                solution.append(str(lib_index) +' '+ str(len(sorted_books)))
                num_lib_selected += 1
                self.scanned_books = self.scanned_books.union(set(sorted_books))
                solution.append(' '.join(str(b) for b in sorted_books))
        print(len(self.scanned_books), file=sys.stderr)
        solution.insert(0, num_lib_selected)
        return solution

b, l, d = [int(s) for s in input().split(" ")]
books = [int(s) for s in input().split(" ")]
libraries = []
lib_books = []
for library in range(l):
    libraries.append([int(s) for s in input().split(" ")])
    lib_books.append([int(s) for s in input().split(" ")])

s = Solution(books, libraries, lib_books, d)
opt_sol=s.get_opt_solution()
for line in opt_sol:
    print(line)
# print(d)
# print(books)
# print(libraries)
# print(lib_books)
