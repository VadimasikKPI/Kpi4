from flask_restful import  reqparse

class Specification:

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)


    def is_satisfied_by(self, client):
        raise NotImplementedError()



class And(Specification):
    def __init__(self, *specifications):
        self.specifications = specifications
    def __and__(self, other):
        if isinstance(other, And):
            self.specifications += other.specifications
        else:
            self.specifications += (other, )
        return self

    def is_satisfied_by(self, candidate, args):
        satisfied = all([
            specification.is_satisfied_by(candidate, args)
            for specification in self.specifications
        ])
        return satisfied



class Or(Specification):
    def __init__(self, *specifications):
        self.specifications = specifications
    def __or__(self, other):
        if isinstance(other, Or):
            self.specifications += other.specifications
        else:
            self.specifications += (other, )
        return self

    def is_satisfied_by(self, candidate, args):
        satisfied = any([
            specification.is_satisfied_by(candidate, args)
            for specification in self.specifications
        ])
        return satisfied


class PackageName(Specification):
  def is_satisfied_by(self, package, args):

      if args['name']:
          return package['name'] == args['name']
      else:
          return True
class MinPrice(Specification):
  def is_satisfied_by(self, package, args):

      if args['min_price']:
          return package['price'] > int(args['min_price'])
      else:
          return True
class MaxPrice(Specification):
  def is_satisfied_by(self, package, args):

      if args['max_price']:
          return package['price'] < int(args['max_price'])
      else:
          return True
