def matrix_multiplier(mat1, mat2):
    result = [[0 for i in range(len(mat2[0]))] for j in range(len(mat1))]

    # iterate through rows of mat1
    for i in range(len(mat1)):
        # iterate through cols of mat2
        for j in range(len(mat2[0])):
            # iterate through rows of mat2
            for k in range(len(mat2)):
                result[i][j] += mat1[i][k] * mat2[k][j]

    return result