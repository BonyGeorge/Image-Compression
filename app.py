import numpy as np
import cv2
import queue


class Node:
    def __init__(self):
        self.prob = None
        self.code = None
        self.data = None
        self.left = None
        self.right = None

    # define rich comparison methods for sorting in the priority queue
    def __lt__(self, other):
        if self.prob < other.prob:
            return 1
        else:
            return 0

    def __ge__(self, other):
        if self.prob > other.prob:
            return 1
        else:
            return 0


def rgb2gray(image):
    grey_img = np.rint(image[:, :, 0] * 0.2989 + image[:, :, 1] * 0.5870 + image[:, :, 2] * 0.1140)
    grey_img = grey_img.astype(int)
    return grey_img


def tree(prob):
    prq = queue.PriorityQueue()
    for color, probability in enumerate(prob):
        leaf = Node()
        leaf.data = color
        leaf.prob = probability
        prq.put(leaf)

    while prq.qsize() > 1:
        newnode = Node()  # create new node
        l = prq.get()
        r = prq.get()  # get the smalles probs in the leaves
        # remove the smallest two leaves
        newnode.left = l  # left is smaller
        newnode.right = r
        newprob = l.prob + r.prob  # the new prob in the new node must be the sum of the other two
        newnode.prob = newprob
        prq.put(newnode)  # new node is inserted as a leaf, replacing the other two
    return prq.get()  # return the root node - tree is complete


# traversal of the tree to generate codes
def huffman_traversal(root, tmp, freq):
    if root.left is not None:
        tmp[huffman_traversal.count] = 1
        huffman_traversal.count += 1
        huffman_traversal(root.left, tmp, freq)
        huffman_traversal.count -= 1

    if root.right is not None:
        tmp[huffman_traversal.count] = 0
        huffman_traversal.count += 1
        huffman_traversal(root.right, tmp, freq)
        huffman_traversal.count -= 1
    else:
        huffman_traversal.output_bits[
            root.data] = huffman_traversal.count  # count the number of bits for each color
        bitstream = ''.join(str(cell) for cell in tmp[1:huffman_traversal.count])
        color = str(root.data)
        wr_str = color + ' ' + bitstream + '\n'
        freq.write(wr_str)  # write the color and the code to a file
    return


# Read an bmp image into a numpy array
img = cv2.imread('test.png')

# convert the image to grayscale
gray_img = rgb2gray(img)

# compute the histogram of pixels
hist = np.bincount(gray_img.ravel(), minlength=256)

# a priority probabilities from frequencies
probabilities = hist / np.sum(hist)

# create the tree using the probabilities.
root = tree(probabilities)

tmp = np.ones([64], dtype=int)
huffman_traversal.output_bits = np.empty(256, dtype=int)
huffman_traversal.count = 0
frequency = open('codes.txt', 'w')

# traverse the tree and write the codes
huffman_traversal(root, tmp, frequency)

# calculate number of bits in grayscale
input_bits = img.shape[0] * img.shape[1] * 8

output_bits = np.sum(huffman_traversal.output_bits * hist)

# compression ratio
compression_ratio = (1 - output_bits / input_bits) * 100

# signal to noise ratio
snr_ratio = pow(output_bits, 2) / pow((output_bits - input_bits), 2)

print('Compression Ratio =  ', round(compression_ratio, 2), ' %')
print('Signal to Noise Ratio = ', round(snr_ratio, 2), ' %')
