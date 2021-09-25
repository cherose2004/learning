def hanoi(n , src , mid , tar):
    if n == 1:
        print("%d->%d" % (src , tar))
        pass
    else:
        hanoi(n-1 , src , tar , mid)
        hanoi(1 , src , mid , tar)
        hanoi(n-1 , mid , src , tar)
        pass
    pass

hanoi(5,1,2,3)