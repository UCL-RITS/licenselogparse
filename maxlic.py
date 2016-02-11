#!/usr/bin/env python3

# This tool runs through a FlexLM license server log and prints the max usage
# of every license type that's checked out from it.

# Owain Kenway, February 2016

# Set the strings we detect as checking a license in/out.
# Maybe should do this as arguments?
LIC_IN = 'IN:'
LIC_OUT = 'OUT:'

# Main function
if __name__ == '__main__':
   import argparse

   parser = argparse.ArgumentParser(description='Print max usage.')
   parser.add_argument('-l', metavar='logfile', type=str, help='Log file.')
   parser.add_argument('-d', action='store_true', help='Enable debug output.')
   parser.add_argument('-u', action='store_true', help='Print users.')
   parser.add_argument('-U', action='store_true', help='Only print users.')

   args = parser.parse_args()

# Debug mode.
   if args.d:
      print(args)

# Some sensible default log.
   logfile = 'logs/test.log'

   if (args.l != None):
      logfile = args.l

   print('Analysing ' + logfile)

# usage and maxusage are dicts that hold the "current" usage and maximum value
# thereof respectively.
   usage = {}
   maxusage = {}

# users list
   users = []
 
   with open(logfile, 'r') as l:
      for line in l:
         fields = line.split()

# Drop any lines with not enough fields to check.
         if len(fields) > 3 :
# For the purposes of this script, a "product" is the (license mananger
# ID) dot the product name.  E.g. (INTEL).CCompL

# Detect checking in a license.
            if (fields[2] == LIC_IN):
# Ansys's LM puts number of license in the sixth field.
               nlic = 1
               if len(fields) == 7: nlic = int(fields[5].strip('('))

# If user hasn't been seen, add the to list of users
               if not fields[4] in users: users.append(fields[4])

               product = fields[1] + '.' + fields[3].strip('"')
# Check to see if we've seen this product before and if so subtract from
# usage.
               if product in usage:
                  usage[product] = usage[product] - nlic
               else:
# Technically if we reach this point the world has gone very wrong.
# But we could also have a partial license file.
# In this instance we want to set the usage of the product to zero.
                  print('WARNING: Checking in license that hasn\'t been checked out. Setting usage for ' + product +  ' to zero.')
                  usage[product] = 0
                  maxusage[product] = 0

# We can't have negative usage but with a partial log file we can.  
# Reset to zero if we get this.
               if usage[product] < 0:
                  print('WARNING: Negative usage detected. Setting usage for ' + product +  ' to zero.')
                  usage[product] = 0
               if args.d: print('in: ' + fields[1] + '.' + fields[3].strip('"') + ': ' + str(usage[product]))

# Detect checking out a license.
            elif (fields[2] == LIC_OUT): 
# Ansys's LM puts number of license in the sixth field.
               nlic = 1
               if len(fields) == 7: nlic = int(fields[5].strip('('))

# If user hasn't been seen, add the to list of users
               if not fields[4] in users: users.append(fields[4])

               product = fields[1] + '.' + fields[3].strip('"')

# If we've seen this product before, add to usage and set maxusage if this
# is the most we've seen so far.
               if product in usage:
                  usage[product] = usage[product] + nlic
                  if maxusage[product] < usage[product]:
                     maxusage[product] = usage[product]
                     if args.d: print('New max for ' + product + ': ' + str(usage[product]))
               else:
# If we've not seen this product before, create new entries in usage and 
# maxusage.
                  usage[product] = nlic
                  maxusage[product] = nlic
               if args.d: print('out: ' + fields[1] + '.' + fields[3].strip('"') + ': ' + str(usage[product]))


   l.close()

# Print the usage for all of the products we've discovered.
   if not args.U:
      print('\nMaximum usage of each product:\n')
      for record in maxusage:
         print(record + ": " + str(maxusage[record])) 

# Print out a user list if we want one.
   if args.u or args.U:
      print('\nUsers who have checked in/out a license:\n')
      for user in users:
         print(user)
