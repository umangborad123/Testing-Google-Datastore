
import webapp2
from google.appengine.ext import db

# define a KIND called "MedicRecord" (like a table)
class MedicRecord(db.Model):
    symptom = db.StringProperty(multiline=False)
    medicine = db.StringProperty(multiline=True)

class MainHandler(webapp2.RequestHandler):

    def get(self):
        # Create the FORM
        self.response.write('<html><body><h1>Online Medical Service</h1>')
        self.response.write(""" <hr> <form method="post">
        Write your symptom:
        <input type="textarea" name="usymptom"></input>
        <p>and its medicine:
        <input type="textarea" name="umedicine"></input><p>
        <input type="submit"></input>
        </form>""")
        self.response.write('</body></html>')

    def post(self):
        # get what the user entered in the FORM
        symptom_entered = self.request.get('usymptom')
        medicine_entered = self.request.get('umedicine')

        # STORE it to the content of an entity of EduRecord table/kind
        mycomment = MedicRecord(symptom=symptom_entered,medicine=medicine_entered)
        mycomment.put()

        # Create the REPLY web page
        self.response.write('<html><body><h1>Make API example</h1>')
        self.response.write('<hr> Previous ITEMS:')

        # Print ALL previous comments stored in Datastore

        # Get SOME entities of the "EduRecord" kind/table
        myquerry = MedicRecord.all()
        myquerry.order("symptom")
        for arecord in myquerry:
           self.response.write('<p>%s = ' % arecord.symptom)
           self.response.write('%s</p>' % arecord.medicine)

class MedicinePage(webapp2.RequestHandler):
    def get(self,asymptom):
        myquerry = MedicRecord.all()
        myquerry.filter('symptom = ',asymptom)
        for arecord in myquerry:
           self.response.write(' %s</p>' % arecord.medicine)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/medic/(.*)', MedicinePage),
], debug=True)
