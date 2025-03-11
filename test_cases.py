# 12 test cases defined
test_cases = [
    # Format: (pc_cons_fx, epsilon)
    (   #Testcase1
        [[-float('inf'), float('inf')],[0,5],[4.0,float('inf')]],
        0.4
    ),
    (    #Testcase2
        [[-float('inf'), float('inf')],[0,5],[1,3],[2,1],[3.0,float('inf')]],
        0.4
    ),
    (    #Testcase3
        [[-float('inf'), float('inf')],[0,1],[1,3],[2,5],[3.0,float('inf')]],
        0.4
    ),
    (    #Testcase4
        [[-float('inf'), float('inf')],[0,1],[1,1.6],[2,2],[3.0,float('inf')]],
        0.6
    ),
    (   #Testcase5
        [[-float('inf'), float('inf')],[0,2.2],[1,1.6],[2,1],[3.0,float('inf')]],
        0.6
    ),
    (   #Testcase6
        [[-float('inf'), float('inf')],[0,1],[1,3],[2,2.5],[3,4],[5,5],[6,3.5],[7.0,float('inf')]],
        0.5
    ),
    (   #Testcase7
        [[-float('inf'), float('inf')],[0.0, 2.1],[2.0, 3.0],[3.0, 3.9],[4.0, 3.8],[5.0, 5.2],[6.0, float('inf')]],
        0.4
    ),
    (   #Testcase8
        [[-float('inf'), float('inf')],[0.0, 2.1],[2.0, 3.0],[3.0, 3.9],[4.0, 3.8],[5.0, 5.2],[6.0, float('inf')]],
        0.8
    ),
    (   #Testcase9
        [[-float('inf'), float('inf')],[0.0, 2.1],[2.0, 3.0],[3.0, 3.9],[4.0, 3.8],[5.0, 5.2],[6.0, float('inf')]],
        2.0
    ),
    (   #Testcase10
        [[-float('inf'), float('inf')],[1.0, 0.0],[2.0, 1.0],[3.0, 0.0],[4.0, -1.0],[5.0, 0.0],[6.0, float('inf')]],
        0.5
    ),
    (  #Testcase11
        [[-float('inf'), float('inf')],[0,5],[1,4.5],[2,3.9],[3,3.5],[4,3],[6,4],[7,4.7],[8,5],[9,float('inf')]],
        0.5
    ),
    (   #Testcase12
        [[-float('inf'), float('inf')],[0, 5.1],[2.0, 6.0],[3.0, 6.1],[4.5, 9.0],[6.0, 4.0],[8.0, float('inf')]],
        2.0
    ),
    (   #Testcase13
        [[-float('inf'), float('inf')], [0, 0.5], [1,2],[2.0, 1.0], [3.0, 3], [4.0, 2], [5.0, 2.7], [6.0, float('inf')]],
        0.1
    )
]

