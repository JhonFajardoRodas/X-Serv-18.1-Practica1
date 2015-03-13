#!/usr/bin/python



import webapp
import cgitb

class cutUrl(webapp.webApp):

	diccUrl = {}
	diccCut = {}
	urlCut = 0
	listaURL = ""

	

	def parse(self, request):
		print("***************\n\n" + request)
		method = request.split(' ', 2)[0]
		resource = request.split()[1][1:]
		
		if method == "POST":
			resource = request.split('\r\n\r\n',1)[1].split("=")[1]
			body = request.split('\r\n\r\n',1)[1]
		else:
			body = ""
		return (method, resource, body)

	def process(self, parseRequest):
		(method, resource, body) = parseRequest

		if not parseRequest:
			httpCode = "404 Not found"
			htmlBody = "<html><body><h1>" + "Not found" + "</body></html>"

		
		if method == "GET":
			if resource == "": 
				formHtml = '<form action="" method="POST">'
				formHtml += 'Introduce URL: <input type= "text" name="valor"'
				formHtml += '<input type="submit">'
				formHtml += '</form>'
				httpCode = "200 OK"
				htmlBody = ("<html><body><h1>" \
							+ formHtml \
							+ str(self.listaURL)
							+ "</body></html>")
			else:
				
				if int(resource) in self.diccCut.keys():
					url = self.diccCut[int(resource)]
					httpCode = "307 REDIRECT"
					
					htmlBody = ("<html><h1>"
								+"<head>"
                                +"<meta http-equiv=Refresh content= 2;url="+url+">"
							    +"<head>"
							    +"</body></html>")

				else:
					httpCode = "404 Not Found"
					htmlBody = "<html><body><h1>" + "No exist URL" + "</body></html>"

		elif method == "POST":
		
			if len(resource.split("http")) != 1:
				resource = resource.replace("%3A%2F%2F", "://") 
				url = resource
			else:
				url = "http://" + resource
			
			if url not in self.diccUrl.keys():
				self.diccUrl[url] = self.urlCut
				self.diccCut[self.urlCut] = url
				self.listaURL += ("<p style=\"font-size: 20px;\">"+"URL solicitada: " 
									+ url + "  ==> URL acortada: [http://localhost:1234/" + str(self.urlCut)+ "]" + "<p>")
				self.urlCut = self.urlCut + 1

			urlCuted = "http://localhost:1234/" + str(self.urlCut -1)
			httpCode = "200 OK"
			htmlBody = ("<html><body><h1>" 
						+ "<a href='" + "http://localhost:1234/" + "'>VOLVER</a>"
						+"<h1><a href='"+ url + "'> " + str(url) + "</a><h1>"
						+"<h1><a href='"+ url+ "'> "  + str(urlCuted) + "</a><h1>"
						+ "</body></html>")

		return (httpCode, htmlBody)

if __name__ == "__main__":
    testWebApp = cutUrl("localhost", 1234)