import gradio as gr
import ast
import random

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
    print("add recipe")
    recipes=get_recipes()
    i=ingridients.split('-')
    recipes.append({"name":name, "ingridients":i, "img":img})
    with open('recipes.json', 'w') as f:
        f.write(recipe)
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
        img_add=gr.Image(type="filepath")
        name_add=gr.TextArea()
        ingridients_add=gr.TextArea()
        recipe_add=gr.TextArea()
        out_add=gr.TextArea()
    b_add_recipe.click(fn=add_recipe,inputs=[img, name_add, ingridients_add, recipe_add],outputs=out_add)


demo.launch(share=False)