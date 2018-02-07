from collections import Counter
import copy
PHRASE = 'iamlordvoldemort'
PHRASE_COUNTS = Counter(PHRASE)


def read_dictionary(fpath):
    with open(fpath) as f:
        for raw_line in f.readlines():
            line = raw_line.strip().lower()
            if len(line) == 0:
                continue

            for letter in line:
                # if the line (word)
                if letter not in PHRASE:
                    break
            else:

                yield line


DICTIONARY = tuple(sorted(set(read_dictionary('american-english'))))

# print('Dictionary', DICTIONARY)


class Node:

    def __init__(self, value, isleaf):
        self.value = value
        self.children = list()
        self.isleaf = isleaf
        self.path = []

    def add_child(self, other_node):
        self.children.append(other_node)

    @property
    def word(self):
        return ''.join(self.path)

    def __str__(self):
        return 'Node: {}, {}, leaf={}'.format(
            str(self.value), self.word, self.isleaf)

    def __repr__(self):
        return 'Node({},{},{})'.format(self.value, self.isleaf)


class SuffixTree:

    def __init__(self, list_of_words):
        self.root = Node(None, False)
        for word in list_of_words:
            # add each word to the suffix tree
            self.traverse(word, True)

    def traverse(self, character_sequence, appending=False):
        cur_node = self.root
        char_iter = iter(character_sequence)
        cur_char = next(char_iter)
        path = []
        while True:
            path.append(cur_char)
            try:
                # assume a matching child node exists
                next_node = [
                    n for n in cur_node.children if n.value == cur_char
                ][0]
            except IndexError:
                # if we're adding to the tree, add a matching child
                # and move on
                if appending:
                    next_node = Node(cur_char, False)
                    next_node.path = path
                    cur_node.add_child(next_node)
                else:
                    return cur_node
            cur_node = next_node
            cur_node.path = path[:]
            # advance the character
            try:
                cur_char = next(char_iter)
            except StopIteration:
                # we have reached the end of the input word
                if appending:
                    cur_node.isleaf = True
                return cur_node


def print_tree(node, indent=1):
    for n in node.children:
        space = (indent - 1) * '.' + '|-'
        print(space + str(n))
        print_tree(n, indent + 1)


def next_partials(tree, word, node, letters):
    for l in set(letters):
        new_word = node.word + l
        found_node = tree.traverse(new_word, False)
        # if it's a valid path in the tree
        if found_node.word == new_word:
            # print('word:', new_word)
            new_letters = letters[:]
            new_letters.remove(l)
            yield dict(
                tree=tree, word=new_word, node=found_node, letters=new_letters)


def voldemort1(sf):
    letters = list(PHRASE)
    stack = [dict(tree=sf, word='', node=sf.root, letters=letters)]
    while len(stack) > 0:
        kwargs = stack.pop()
        # print(kwargs)
        for partial in next_partials(**kwargs):
            n = partial['node']
            w = partial['word']
            if n.isleaf and w == n.word:
                yield n
                # print(w, sf.traverse(w).isleaf)
            stack.append(partial)


memory = dict()
dictionary_memory = dict()


def v2partials(words=None):
    # import pudb
    # pudb.set_trace()
    # print(words)
    if words is None:
        words = Counter()
    else:
        # print(words)
        words = dict(words)
    combined = ''.join(k * v for k, v in words.items())
    # ========== memoization ==========
    results = []
    frozen_words = frozenset(sorted(words.items()))
    if frozen_words in memory:
        return memory[frozen_words]
    if frozen_words in dictionary_memory:
        cur_dictionary = dictionary_memory[frozen_words]
    else:
        cur_dictionary = set(DICTIONARY)

    for w in sorted(cur_dictionary):
        # potential words
        new_letter_counts = Counter(w + combined)
        for letter in new_letter_counts:
            if new_letter_counts[letter] > PHRASE_COUNTS[letter]:
                # print('exclude',words + [w])
                cur_dictionary.remove(w)
                # print('discard', w, words)
                break
        else:
            outc = Counter(words)
            outc[w] += 1
            out = frozenset(outc.items())
            results.append(out)
    dictionary_memory[frozen_words] = set(cur_dictionary)
    memory[frozen_words] = sorted(results)
    return results


def voldemort2(dictionary):

    stack = []
    for p in v2partials(words=None):
        # print('preloaded:', p)
        stack.append(p)
    while len(stack) > 0:
        args = stack.pop()
        # print(args)
        for x in v2partials(args):
            # print('x', x)
            partial_solution = Counter()
            for k, v in dict(x).items():
                partial_solution.update(k * v)
            # print(partial_solution)
            if partial_solution == PHRASE_COUNTS:
                # if sum(partial_solution.values()) > 1:
                # print('yielded', x['words'])
                yield Counter(dict(x))
            else:
                stack.append(x)


def main():
    # sf = SuffixTree(read_dictionary('american-english'))
    # for n in voldemort1(sf):
    #     print(n.word)

    p = "aaronloveslindsay"
    c = 0
    pc = Counter(p)
    for w in DICTIONARY:
        wc = Counter(w)
        for k, v in wc.items():
            if v > pc[k] or len(w) < 3:
                break
        else:
            c += 1
            print(w)
    print(c)

    quit()
    seen = set()
    for w in voldemort2(DICTIONARY):
        # for w in voldemort2(['marvel', 'motor']):
        dw = tuple(sorted(dict(w).items()))
        if dw not in seen:
            print(dict(w))
            seen.add(dw)
        # pass


if __name__ == '__main__':
    main()
