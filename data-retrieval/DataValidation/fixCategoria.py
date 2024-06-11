import json

def fix_categoria():
    with open('./news_data/2019/key_moments_photos_2019_tmp2.json', 'r') as f:
        data = json.load(f)
    
    # Define categories and subcategories
    categorias = ['Secções', 'Local', 'Opinião', 'Editorial']
    subcategorias = {
        'Secções': ['Centrais', 'Actualidade', 'Religião', 'Desporto', 'Cultura', 'Economia', 'Associativismo', 'Agenda'],
        'Local': ['Covilhã', 'Fundão', 'Castelo Branco', 'Belmonte', 'Guarda', 'Região']
    }
    
    # Loop through articles and update categories and subcategories
    for article in data:
        for subcategoria, sublista in subcategorias.items():
            for item in article['category'].split():  # Split the category string into individual words
                if item.strip() in sublista:
                    article['category'] = subcategoria
                    article['sub_category'] = item.strip()  # Set subcategory
                    break
            else:
                continue
            break
        else:
            for categoria in categorias:
                if categoria in article['category']:
                    if categoria in subcategorias:
                        for subcategoria in subcategorias[categoria]:
                            if subcategoria in article['title']:
                                article['sub_category'] = subcategoria
                                break
                        else:
                            article['sub_category'] = categoria  # Default to category if no subcategory found
                    else:
                        article['sub_category'] = categoria  # Default to category if no subcategory found
                    break
    
    # Write back to the JSON file
    with open('./news_data/2019/key_moments_photos_2019_tmp3.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  # Dump updated data back to the file with indentation

# Call the function to fix categorization
fix_categoria()
