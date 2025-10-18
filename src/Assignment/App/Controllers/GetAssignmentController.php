<?php

declare(strict_types=1);

namespace Src\Assignment\App\Controllers;

use Illuminate\Http\JsonResponse;
use Src\Assignment\App\Resources\AssignmentResource;
use Src\Assignment\Domain\Model\Assignment;

class GetAssignmentController
{
    public function __invoke(Assignment $assignment): JsonResponse
    {
        return AssignmentResource::make($assignment)->response();
    }
}
