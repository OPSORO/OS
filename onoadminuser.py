class OnoAdminUser(object):
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return "admin"

	def is_admin(self):
		return True
