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
        return("Images/Not_found.png","No recipe found")

def get_recipes():
    recipes=open('recipes.json', 'r').read()
    recipes=ast.literal_eval(recipes)
    return(recipes)

def add_recipe(img, name, ingredients, recipe, f1_add, f2_add, f3_add):
    print(f1_add)
    img=Image.open(img)
    w, h = img.size 
    print(w)
    print(h)
    print(h*(600/w))
    img = img.resize( (600, (int(h*(600/w))) ) )
    n=name.replace(" ","_")
    path="Images/"+n+".jpg"
    img.save(path)
    print("add recipe")
    recipes=get_recipes()
    i=ingredients.split('\n')
    filters=f1_add+f2_add+f3_add
    recipes.append({"name":name, "ingredients":i, "recipe":recipe, "img":path, "filters": filters})
    recipes=str(recipes)
    recipes=recipes.replace("'",'"')
    for i in range (1,len(recipes)-1):
        if(recipes[i]=='"' and recipes[i-1].isalpha() and recipes[i+1].isalpha()):
            recipes=recipes[:i]+"'"+recipes[i+1:]
    
    with open('recipes.json', 'w') as f:
        f.write(str(recipes))
    return("Done")

def update_filters(check):
    print(check)
    pass

def remove(name):
    recipes=get_recipes()
    pos=-1
    for i in range(len(recipes)):
        if(recipes[i]['name']==name):
            pos=i
            break
    if (pos!=-1):
        recipes.pop(pos)
        recipes=str(recipes)
        recipes=recipes.replace("'",'"')
        for i in range (1,len(recipes)-1):
            if(recipes[i]=='"' and recipes[i-1].isalpha() and recipes[i+1].isalpha()):
                recipes=recipes[:i]+"'"+recipes[i+1:]
        with open('recipes.json', 'w') as f:
            f.write(str(recipes))
        return("Done")
    else:
        return("Not found")
        






with gr.Blocks() as demo:
    gr.Markdown("# Recipe Manager")
    gr.Markdown('## Find a recipe: ')
    f1=gr.CheckboxGroup(["Sweet", "Savory"], label="")
    f2=gr.CheckboxGroup(["Breakfast", "Lunch", "Dinner"], label="")
    f3=gr.CheckboxGroup(["First Course", "Main course", "Second course","Side", "Desserts","Drinks"], label="")

    b_random_recipe=gr.Button("Random recipe")
    with gr.Row():
        img=gr.Image(type="filepath", label="Result: ")
        ricetta=gr.TextArea(label="Recipe: ")

    gr.Markdown('## Add new recipe: ')        
    f1_add=gr.CheckboxGroup(["Sweet", "Savory"], label="")
    f2_add=gr.CheckboxGroup(["Breakfast", "Lunch", "Dinner"], label="")
    f3_add=gr.CheckboxGroup(["First Course", "Main course", "Second course","Side", "Desserts","Drinks"], label="")
    with gr.Row():
        img_add=gr.Image(type="filepath", label="Result:")
        name_add=gr.TextArea(label="Name: ")
        ingridients_add=gr.TextArea(label="Ingredients: ")
        #value="write in the format:\nIngredientd1\nIngredientd2\n...",
        recipe_add=gr.TextArea(label="Recipe: ")
    out_add=gr.Textbox(label="Result: ") 
    b_add_recipe=gr.Button("Add recipe")

    gr.Markdown("## Remove recipe")
    recipe_remove=gr.Textbox(label="Name: ")
    out_remove=gr.Textbox(label="Result: ")
    b_remove=gr.Button("Remove")
    


    b_random_recipe.click(fn=display_recipe, inputs=[f1,f2,f3], outputs=[img,ricetta])
    b_add_recipe.click(fn=add_recipe, inputs=[img_add, name_add, ingridients_add, recipe_add, f1_add, f2_add, f3_add], outputs=[out_add])
    b_remove.click(fn=remove, inputs=[recipe_remove], outputs=[out_remove])


demo.launch(share=False)