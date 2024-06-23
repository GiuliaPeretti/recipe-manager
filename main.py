import gradio as gr
import ast
import random
import PIL
from PIL import Image
def display_recipe():
    recipes=get_recipes()
    n=random.randint(0, len(recipes)-1)
    recipe=recipes[n]
    r=recipe['name']+'\n'+"Ingredients"+'\n'
    ing=recipe['ingredients']
    for i in range(len(ing)):
        r=r+str(i)+') '+ing[i]+'\n'
    return(recipe['img'], r)

def get_recipes():
    recipes=open('recipes.json', 'r').read()
    recipes=ast.literal_eval(recipes)
    return(recipes)

def add_recipe(img, name, ingridients, recipe):
    # img=Image.open(img)
    path="Images/"+name+".webp"
    img.save(path)
    print("add recipe")
    recipes=get_recipes()
    i=ingridients.split('\n')
    recipes.append({"name":name, "ingridients":i, "img":path})
    recipes=str(recipes)
    recipes=recipes.replace("'",'"')
    with open('recipes.json', 'w') as f:
        f.write(str(recipes))
    return("added")






with gr.Blocks() as demo:
    gr.Markdown("# Recipe Manager")
    b_random_recipe=gr.Button("Random recipe")
    with gr.Row():
        img=gr.Image(type="filepath")
        ricetta=gr.TextArea()
    b_random_recipe.click(fn=display_recipe, outputs=[img,ricetta])
    b_add_recipe=gr.Button("Add recipe")
    with gr.Row():
        img_add=gr.Image("filepath")
        name_add=gr.TextArea()
        ingridients_add=gr.TextArea()
        recipe_add=gr.TextArea()
        out_add=gr.TextArea()
    b_add_recipe.click(fn=add_recipe,inputs=[img_add, name_add, ingridients_add, recipe_add],outputs=out_add)


demo.launch(share=False)