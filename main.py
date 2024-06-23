import gradio as gr
import ast
import random
from PIL import Image

def display_recipe(f1,f2,f3):
    filters=f1+f2+f3
    recipes=get_recipes()
    valid_recipes=[]
    for i in range(len(recipes)):
        print("Checking "+str(i))
        found_all=True
        for f in filters:
            print("checking "+f)
            found=False
            for r in recipes[i]['filters']:
                print(r)
                if(f==r):
                    print("filter trovato")
                    found=True
                    break
            if(not(found)):
                print("filter non trovato")
                found_all=False
                break
        if(found_all):
            print("trovati filtri")
            valid_recipes.append(i)
    print(valid_recipes)
    if(len(valid_recipes)!=0):
        n=random.choice(valid_recipes)
        recipe=recipes[n]
        r=recipe['name']+'\n\n'+"Ingredients:"+'\n'
        ing=recipe['ingredients']
        for i in range(len(ing)):
            r=r+str(i)+') '+ing[i]+'\n'
        r=r+"\nRecipe: \n"+recipe['recipe']
        return(recipe['img'], r)
    else:
        return("Images\Not_found.png","")

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

def update_filters(check):
    print(check)
    pass




with gr.Blocks() as demo:
    gr.Markdown("# Recipe Manager")
    f1=gr.CheckboxGroup(["Sweet", "Savory"], label="")
    f2=gr.CheckboxGroup(["Breakfast", "Lunch", "Dinner"], label="")
    f3=gr.CheckboxGroup(["First Course", "Main course", "Second course","Side", "Desserts","Drinks"], label="")

    b_random_recipe=gr.Button("Random recipe")
    with gr.Row():
        img=gr.Image(type="filepath", label="Result: ")
        ricetta=gr.TextArea(label="Recipe: ")
    b_add_recipe=gr.Button("Add recipe")
    with gr.Row():
        img_add=gr.Image(type="filepath", label="Result:")
        name_add=gr.TextArea(label="Name: ")
        ingridients_add=gr.TextArea(label="Ingredients: ")
        #value="write in the format:\nIngredientd1\nIngredientd2\n...",
        recipe_add=gr.TextArea(label="Recipe: ")
        out_add=gr.TextArea()

    b_random_recipe.click(fn=display_recipe, inputs=[f1,f2,f3], outputs=[img,ricetta])
    b_add_recipe.click(fn=add_recipe,inputs=[img_add, name_add, ingridients_add, recipe_add],outputs=out_add)
    # f1_check.change(fn=update_filters,inputs=[f1_check],outputs=[])



demo.launch(share=False)