# Automatically generated by pb2py
# fmt: off
import protobuf as p


class TronProposalApproveContract(p.MessageType):

    def __init__(
        self,
        proposal_id: int = None,
        is_add_approval: bool = None,
    ) -> None:
        self.proposal_id = proposal_id
        self.is_add_approval = is_add_approval

    @classmethod
    def get_fields(cls):
        return {
            1: ('proposal_id', p.UVarintType, 0),
            2: ('is_add_approval', p.BoolType, 0),
        }
