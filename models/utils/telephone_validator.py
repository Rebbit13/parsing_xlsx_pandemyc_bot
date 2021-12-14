def form_valid_telephone(telephone: str):
    telephone = telephone.replace("+", "").replace("-", "").replace("(", "").replace(")", "")
    check = False
    if len(telephone) == 11:
        if telephone[0:2] == "89" or telephone[0:2] == "79":
            telephone = "8" + telephone[1:]
            check = True
    elif len(telephone) == 10:
        if telephone[0] == "9":
            telephone = "8" + telephone[1:]
            check = True
    return telephone, check
