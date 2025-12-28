from flask import Blueprint
from flask import redirect,render_template,request,url_for,jsonify,session
from app.__init__ import mysql
import os
from dotenv import load_dotenv

load_dotenv()  # for accesssing secret key from .env 


api_bp = Blueprint('api',__name__,'/api')

# api/documentation
@api_bp.route('/api/docs')
def api_docs():
    return jsonify({
        'api_name': 'Local Service Connect API',
        'version': '1.0',
        'endpoints': {
            '/api/services': {
                'method': 'GET',
                'description': 'Get all available services',
                'parameters': {
                    'category': 'Filter by category (optional)',
                    'limit': 'Number of results (optional)'
                },
                'example': 'GET /api/services?category=plumbing&limit=5'
            },
            '/api/services/<id>': {
                'method': 'GET', 
                'description': 'Get single service by ID',
                'example': 'GET /api/services/5'
            }
        },
        'base_url': 'http://localhost:5000',
        'created_by': 'Muhammad Hammad'
    })

# show all users API: 1
@api_bp.route('/api/users')
def get_users():
   # connection 
   try:
      cursor = mysql.connection.cursor()
      print('runnn')

      # get users data
      cursor.execute(' SELECT id,username,email FROM users LIMIT 10')
      usersData = cursor.fetchall()
      cursor.close()

      return jsonify({
         'success' : True,
         'count' : len(usersData),
         'users' : usersData
      })
   
   except Exception as e:
      return jsonify({ 'error':str(e)}) , 500


# show specific user
@api_bp.route('/api/user/<int:user_id>')
def getUser(user_id):
   # make connection
   try:

      cursor= mysql.connection.cursor()

      # get specific user
      cursor.execute(' SELECT * FROM users WHERE id = %s',(user_id,))
      userData = cursor.fetchall()
      cursor.close()

      return jsonify({
         'success' : True,
         'userID' : user_id,
         'userData' : userData
      })
   except Exception as e:
      return jsonify({
         'error' : str(e)
      }), 500

   
# services api
@api_bp.route('/api/services')
def getServices():
   # connection
   try:

      cursor = mysql.connection.cursor()
      cursor.execute(' SELECT id,service_name,description,price FROM services LIMIT 20')
      services = cursor.fetchall()
      cursor.close()

      # check 
      if services:
         return jsonify({
            'success' : True,
            'total' : len(services),
            'services' : services
         })
      else:
         return jsonify({
            'error' : 'No services found'
         })
      
   except Exception as e:
      return jsonify({
         'error' : str(e)
      }), 500


# api for bookings data

# for all bookings
@api_bp.route('/api/bookings')
def getBookingsData():
   # first make conn with db()
   try:
      cursor = mysql.connection.cursor()
      # fetch
      cursor.execute(' SELECT id,user_id,provider_id,created_at,service_type,service_description FROM bookings')
      bookingData = cursor.fetchall()

      if bookingData:
         return jsonify({
            'success': True,
            'lenght' : len(bookingData),
            'bookingData': bookingData
         })
      else:
         return jsonify({
            'error': "No data found!"
         })
   
   except Exception as e:
      return jsonify({
         'success': False,
         'error' : str(e)
      }),401

# for specific user
@api_bp.route('/api/bookings/<int:user_id>')
def bookingsByUserid(user_id):
   # first make conn with db()
   username = session.get('username')
   try:
      cursor = mysql.connection.cursor()
      # fetch
      cursor.execute(' SELECT id,user_id,provider_id,created_at,service_type,service_description FROM bookings WHERE user_id=%s',(user_id,))
      bookingData = cursor.fetchall()

      if bookingData:
         return jsonify({
            'success': True,
            'Username/CustomerName' :username,
            'lenght' : len(bookingData),
            'bookingData': bookingData
         })
      else:
         return jsonify({
            'error': "No data found!"
         })
   
   except Exception as e:
      return jsonify({
         'success': False,
         'error' : str(e)
      }),401
   


# for specific user with status
@api_bp.route('/api/bookings/<int:user_id>/')
def bookingsByStatus(user_id):
   # first make conn with db()
   status = request.args.get('status')
   username = session.get('username')
   try:
      cursor = mysql.connection.cursor()
      # fetch
      cursor.execute(' SELECT id,user_id,provider_id,created_at,service_type,service_description FROM bookings WHERE user_id=%s AND status =%s',(user_id,status))
      bookingData = cursor.fetchall()

      if bookingData:
         return jsonify({
            'success': True,
            'Username/CustomerName' :username,
            'status':status,
            'lenght' : len(bookingData),
            'bookingData': bookingData
         })
      else:
         return jsonify({
            'error': "No data found!"
         })
   
   except Exception as e:
      return jsonify({
         'success': False,
         'error' : str(e)
      }),401