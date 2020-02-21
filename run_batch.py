import glob
from statistics import median


class GeneralInformation:
    def __init__(self, books, libraries, number_of_days, books_scores):
        self.total_amount_of_books = books
        self.total_amount_of_libraries = libraries
        self.number_of_days = number_of_days
        self.book_scores = books_scores


class Library:
    def __init__(self, books, sign_up_time, books_send_per_day, books_in_library):
        self.total_amount_of_books = books
        self.sign_up_time = sign_up_time
        self.books_send_per_day = books_send_per_day
        self.books_in_library = books_in_library


def parse_inputs(input_file):
    with open(input_file) as f:
        content = f.readlines()

    first_line = content[0].split()

    books = int(first_line[0])
    libraries = int(first_line[1])
    number_of_days = int(first_line[2])
    all_scores_for_books = list(map(int, content[1].split()))

    general_info = GeneralInformation(books, libraries, number_of_days, all_scores_for_books)

    content = content[2:]

    all_libraries = []

    for index_library in range(0, len(content) - 1, 2):
        first_line = list(map(int, content[index_library].split()))
        second_line = list(map(int, content[index_library + 1].split()))

        all_libraries.append(Library(first_line[0], first_line[1], first_line[2], second_line))

    return general_info, all_libraries


def get_book_scores(all_book_scores, library_books):
    return [all_book_scores[b] for b in library_books]


def sort_list_and_keep_indices(values, indexes, reverse=True):
    return zip(*sorted(zip(values, indexes), reverse=reverse))


def sort_libraries(general_info, all_libraries):
    library_score = []

    for library in all_libraries:
        book_scores = get_book_scores(general_info.book_scores, library.books_in_library)

        m_score = (median(book_scores)) / library.sign_up_time
        library_score.append(m_score)

    highest_scores, indexes = sort_list_and_keep_indices(library_score, range(0, len(library_score)))

    return highest_scores, indexes


def run_main(input_file):
    general_info, all_libraries = parse_inputs(input_file)
    assert general_info.total_amount_of_libraries == len(all_libraries)

    return input_file

if __name__ == '__main__':
    for file in glob.glob("./input/*.txt"):
        run_main(file)
