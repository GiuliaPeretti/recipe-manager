import gradio as gr
import ast
import random
import PIL
from PIL import Image
def display_recipe():
    recipes=get_recipes()
    n=random.randint(0, len(recipes)-1)
    recipe=recipes[n]
    r=recipe['name']+'\n\n'+"Ingredients:"+'\n'
    ing=recipe['ingredients']
    for i in range(len(ing)):
        r=r+str(i)+') '+ing[i]+'\n'
    r=r+"\nRecipe: \n"+recipe['recipe']
    return(recipe['img'], r)

def get_recipes():
    recipes=open('recipes.json', 'r').read()
    recipes=ast.literal_eval(recipes)
    return(recipes)

def add_recipe(img, name, ingredients, recipe):
    img=Image.open(img)
    path="Images/"+name+".webp"
    img.save(path)
    print("add recipe")
    recipes=get_recipes()
    i=ingredients.split('\n')
    recipes.append({"name":name, "ingredients":i, "img":path})
    recipes=str(recipes)
    recipes=recipes.replace("'",'"')
    with open('recipes.json', 'w') as f:
        f.write(str(recipes))
    return("added")






with gr.Blocks() as demo:
    gr.Markdown("# Recipe Manager")
    gr.CheckboxGroup(["Sweet", "Savory"], label="Countries", info="Where are they from?")
    gr.CheckboxGroup(["Breakfast", "Lunch", "Dinner"], label="Countries", info="Where are they from?")
    gr.CheckboxGroup(["First Course", "Main course", "Second course","Side", "Desserts","Drinks"], label="Countries", info="Where are they from?")



    b_random_recipe=gr.Button("Random recipe")
    with gr.Row():
        img=gr.Image(type="filepath", label="Result: ")
        ricetta=gr.TextArea(label="Recipe: ")
    b_random_recipe.click(fn=display_recipe, outputs=[img,ricetta])
    b_add_recipe=gr.Button("Add recipe")
    with gr.Row():
        img_add=gr.Image(type="filepath", label="Result:")
        name_add=gr.TextArea(label="Name: ")
        ingridients_add=gr.TextArea(label="Ingredients: ")
        #value="write in the format:\nIngredientd1\nIngredientd2\n...",
        recipe_add=gr.TextArea(label="Recipe: ")
        out_add=gr.TextArea()
    b_add_recipe.click(fn=add_recipe,inputs=[img_add, name_add, ingridients_add, recipe_add],outputs=out_add)


demo.launch(share=False)