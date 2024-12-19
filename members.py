from flask import Blueprint, request, jsonify

members_bp = Blueprint('members', __name__)

members = {} #temporary data storage for API testing.

@members_bp.route('/members', methods=['POST'])
def add_member():
    data = request.json
    if not data.get('name') or not data.get('email') or not data.get('type'):
        return jsonify({'error': 'Name, email, and type are required'}), 400

    if data['type'] not in ['student', 'staff']:
        return jsonify({'error': 'Invalid member type. Must be "student" or "staff"'}), 400

    member_id = len(members) + 1
    members[member_id] = {
        'id': member_id,
        'name': data['name'],
        'email': data['email'],
        'phone': data.get('phone', None),
        'type': data['type']
    }
    return jsonify({'message': 'New member Added', 'member': members[member_id]}), 201



@members_bp.route('/members', methods=['GET'])
def get_members_or_member():
    member_id = request.args.get('id')  # Get the 'id' query parameter
    member_type = request.args.get('type')  # Get the 'type' query parameter

    if member_id:
        # Fetch a specific member by ID
        member = members.get(int(member_id))  # Convert `member_id` to int
        if member:
            return jsonify({'member': member}), 200
        return jsonify({'error': 'Member not found'}), 404

    if member_type:
        if member_type not in ['student', 'staff']:
            return jsonify({'error': 'Invalid member type. Must be "student" or "staff"'}), 400

        # Filter members by type
        filtered_members = {id: member for id, member in members.items() if member['type'] == member_type}
        return jsonify({'members': filtered_members}), 200

    # Return all members if no query parameters are provided
    return jsonify({'members': members}), 200




@members_bp.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    if member_id not in members:
        return jsonify({'error': 'Member not found'}), 404

    data = request.json
    member = members[member_id]
    member['name'] = data.get('name', member['name'])
    member['email'] = data.get('email', member['email'])
    member['phone'] = data.get('phone', member.get('phone'))
    if 'type' in data:
        if data['type'] not in ['student', 'staff']:
            return jsonify({'error': 'Invalid member type. Must be "student" or "staff"'}), 400
        member['type'] = data['type']
    return jsonify({'message': 'Member updated', 'member': member}), 200


@members_bp.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if member_id in members:
        del members[member_id]
        return jsonify({'message': 'Member deleted'}), 200
    return jsonify({'error': 'Member not found'}), 404
