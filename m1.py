sessionTable = {"k": "a"}

if __name__ == "__main__":
    import m2
    sessionTable["l"] = "c"
    m2.pprint(sessionTable)
    sessionTable["aa"] = "ca"
    m2.pprint(sessionTable)
