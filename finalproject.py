from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from databasesetup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine))
@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    restaurants = session.query(Restaurant).all()
    #print ("name " restaurant.name)
    return render_template('restaurants.html', restaurants = restaurants)
@app.route('/restaurants/new/', methods =['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurantName = request.form['name']
        newRestaurant = Restaurant(name = restaurantName)
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurantItem = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newRestaurantName = request.form['name']

        restaurantItem.name = newRestaurantName
        session.add(restaurantItem)
        session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant = restaurantItem)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantItem = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantItem)
        session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurantItem)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],price = request.form['price'], description = request.form['desc'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method =='POST':
        newName = request.form['name']
        newPrice = request.form['price']
        newDescription = request.form['desc']
        newCourse = request.form['course']
        if newName != "":
            menuItem.name = newName
        if newPrice != "":
            menuItem.price = newPrice
        if newDescription != "":
            menuItem.description =newDescription
        if newCourse !="":
            menuItem.course = newCourse
        session.add(menuItem)
        session.commit()
        flash("Menu item updated")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenu.html', menuItem = menuItem, restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    print ("name: " + str(menuItem.name))
    print ("id: " +str(menuItem.id))
    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash("Menu Item deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delmenuitem.html', menuItem = menuItem, restaurant_id=restaurant_id)



if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
