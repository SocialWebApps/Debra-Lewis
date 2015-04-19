from bs4 import BeautifulSoup
import bs4.element as BSElementType


# This function is available in the file "GetRecipeFromURL.py" 
# in the "resources" folder off of the directory that contains this notebook.
def getTagInfo(tag):
    #make sure it's the right kind of input, or else you'll get all kinds of weird errors.
    if type(tag) is not BSElementType.Tag:
         return "INVALID INPUT!"
    
    tagInfo = ""
    
    # See if the input tag has a 'content' attribute.
    # If it does, use whatever text is stored in that attribute as the name of the recipe
    if tag.has_attr('content'):
        tagInfo = tag.get('content')
        
    # See if fn is empty (there was no "content" attribute, or it was empty)
    if not tagInfo:
        # Grab whatever text is in the tag
        # For example, for <p>blah</p>, it would grab "blah"
        tagInfo = tag.get_text()
        
        #if function STILL hasn't gotten any info by this point, then just set it to "None"
        if not tagInfo:
            tagInfo = "None"
        
    return tagInfo.strip()
	
	
"""
" Extracts information from a website that uses the Recipe scheme from schema.org (schema.org/Recipe)
" Information extracted is: recipe name; author name; ingredients; instructions
"""
def parse_recipe(url):
    req = requests.get(URL)
    
    soup = BeautifulSoup(req.text)
    
    recipe = soup.find(itemtype="http://schema.org/Recipe")

    if recipe and len(recipe) > 1:      
        #Get recipe name:
        fn = getTagInfo(recipe.find(itemprop="name"))
        
        #Get author info:
        foodByline = recipe.find(itemprop="author")
        foodAuthor = foodByline.find(itemprop="name")
        author = getTagInfo(foodAuthor)

        #Get ingredient information:
        ingredients = [i.string 
                            for i in recipe.findAll(itemprop="ingredients") 
                                if i.string is not None] 

        instructions = []  #instructions
        for i in recipe.find(itemprop="recipeInstructions"):
            if type(i) == BSElementType.Tag:
                s = ''.join(i.findAll(text=True)).strip()
            elif type(i) == BSElementType.NavigableString:
                s = i.string.strip()
            else:
                continue

            if s != '': 
                instructions += [s]

        return {
            'name': fn,
            'author': author,
            'ingredients': ingredients, 
            'instructions': instructions,
            }
    else:
        return {}