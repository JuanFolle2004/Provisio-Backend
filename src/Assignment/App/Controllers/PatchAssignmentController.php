<?php

declare(strict_types=1);

namespace Src\Assignment\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Assignment\App\Request\PatchAssignmentRequest;
use Src\Assignment\App\Resources\AssignmentResource;
use Src\Assignment\Domain\Model\Assignment;
use Src\Users\Domain\Models\User;
use Throwable;

class PatchAssignmentController
{
    /**
     * @throws Throwable
     */
    public function __invoke(
        PatchAssignmentRequest $patchAssignmentRequest,
        #[CurrentUser]
        User $currentUser,
    ): JsonResponse {
        $dto = $patchAssignmentRequest->toDto();
        $assignment = Assignment::findOrFail($dto->assignmentId);

        $assignment->bought = $dto->bought;
        $assignment->amount = $dto->amount;
        $assignment->saveOrFail();

        return AssignmentResource::make($assignment)->response();
    }
}
