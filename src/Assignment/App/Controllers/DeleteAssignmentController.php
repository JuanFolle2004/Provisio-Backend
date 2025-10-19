<?php

declare(strict_types=1);

namespace Src\Assignment\App\Controllers;

use Illuminate\Http\JsonResponse;
use Src\Assignment\Domain\Model\Assignment;

class DeleteAssignmentController
{
    public function __invoke(Assignment $assignment): JsonResponse
    {
        $assignment->delete();

        return response()->json(null, 20);
    }
}
