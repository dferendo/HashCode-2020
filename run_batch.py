import glob
from statistics import median


class GeneralInformation:
    def __init__(self, books, libraries, number_of_days, books_scores):
        self.total_amount_of_books = books
        self.total_amount_of_libraries = libraries
        self.number_of_days = number_of_days
        self.book_scores = books_scores


class Library:
    def __init__(self, index, books, sign_up_time, books_send_per_day, books_in_library):
        self.index = index
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
    current_library = 0

    for index_library in range(0, len(content) - 1, 2):
        first_line = list(map(int, content[index_library].split()))
        second_line = list(map(int, content[index_library + 1].split()))

        all_libraries.append(Library(current_library, first_line[0], first_line[1], first_line[2], second_line))
        current_library += 1

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


def send_books(general_info, all_libraries, sorted_libraries_indexes):
    # Library signup variables
    active_libraries = []
    library_index = 0
    next_active_library_day = 0
    next_active_library = None

    # Sending books variables
    books_sent = set()
    libraries_with_sent_books = {}

    for current_day in range(0, general_info.number_of_days):
        # Library signup
        if next_active_library is None:
            # All libraries are added
            if len(active_libraries) < general_info.total_amount_of_libraries:
                next_active_library = all_libraries[sorted_libraries_indexes[library_index]]
                next_active_library_day += next_active_library.sign_up_time
                library_index += 1

        for library in active_libraries:
            # Get the biggest book
            books_of_library = set(library.books_in_library)
            books_that_can_be_sent = books_of_library - books_sent

            if len(books_that_can_be_sent) == 0:
                continue

            scores_of_books_that_can_be_sent = get_book_scores(general_info.book_scores, library.books_in_library)
            temp_1, index_1_temp = sort_list_and_keep_indices(scores_of_books_that_can_be_sent, list(books_that_can_be_sent))

            current_books_sent = 0

            for book_that_can_be_sent in index_1_temp:
                if current_books_sent == library.books_send_per_day:
                    break

                books_sent.add(book_that_can_be_sent)

                if library.index not in libraries_with_sent_books:
                    libraries_with_sent_books[library.index] = [book_that_can_be_sent]
                else:
                    libraries_with_sent_books[library.index].append(book_that_can_be_sent)

                current_books_sent += 1

        # Libraries cannot send book when they are added (Thus, done last)
        if next_active_library_day == current_day:
            active_libraries.append(next_active_library)
            next_active_library = None

    return active_libraries, libraries_with_sent_books


def output(ordered_libraries, libraries_with_sent_books, count_out):
    with open(f'output/output{count_out}.txt', 'w') as file:
        file.write(str(len(libraries_with_sent_books)) + '\n')

        for signed_up_library in ordered_libraries:
            if signed_up_library.index not in libraries_with_sent_books:
                continue

            file.write(str(signed_up_library.index) + ' ' + str(len(libraries_with_sent_books[signed_up_library.index])) + '\n')
            file.write(' '.join(map(str, libraries_with_sent_books[signed_up_library.index])) + '\n')


def run_main(input_file, index):
    general_info, all_libraries = parse_inputs(input_file)
    assert general_info.total_amount_of_libraries == len(all_libraries)

    _, indexes = sort_libraries(general_info, all_libraries)
    ordered_libraries, libraries_with_sent_books = send_books(general_info, all_libraries, indexes)

    output(ordered_libraries, libraries_with_sent_books, index)


if __name__ == '__main__':
    for index, file in enumerate(glob.glob("./input/*.txt")):
        run_main(file, index)
