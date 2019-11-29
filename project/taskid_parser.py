

def parse(tasID):
    return tasID.replace(":", "_")

if __name__ == "__main__":
    print(parse("fd-L:20191129151942:5065:ceshi62yq-consumer-group"))
