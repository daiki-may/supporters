import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/Users/hiroki-is/IdeaProjects/testing/gikucamp-firebase-adminsdk-bw43u-2fb954e096.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
ref = db.collection(u'data')
docs = ref.stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
###################################################################################


input_cvdata = 777
####################################################################################
doc_ref = db.collection(u'data').document(u'90TwVL13wTuPpmCgw24C')
doc_ref.set({
    u'amount': f"{input_cvdata}",
})