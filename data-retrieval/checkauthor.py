# Assuming you have already defined news_item['author']

male_names = ["João", "Manuel", "Rui", "Carlos", "José", "António", "Francisco", "Luís", "Pedro", "Paulo", "Vítor", "Filipe", "Avelino", "Eduardo", "Joaquim", "Jorge", "Tiago", "Alberto", "Vítor", "Vitor", "Ricardo", "Sérgio", "Ayres", "Carlos"]
female_names = ["Ana", "Maria", "Susana", "Cristela", "Neuza", "Maria Eduarda", "Assunção", "Susana", "Ana Rita", "Maria Eduarda", "Maria", "Cristela", "Maria"]

author = "Assunção Vaz Patto"

# Check if any part of the author's name matches the names in the lists
is_male = any(name in author for name in male_names)
is_female = any(name in author for name in female_names)

if is_male and not is_female:
    print("The author is male")
elif is_female and not is_male:
    print("The author is female")
else:
    print("The gender of the author is unknown")